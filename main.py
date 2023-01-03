import aiohttp
import flask, aiosqlite, discord
import httpx
from oAuthMethods import AuthMethods
from utils import *
from flask import request, make_response, redirect

path = r'database.db'
app = flask.Flask(__name__, template_folder="html")
config = LoadJson()
SecretKey = config['SecretKey']
RedirectURL = config['oAuthURL']
GuildID = config['GuildID']

@app.route('/join', methods=['GET'])
async def MainRoute():
    Code = request.args.get('code')

    async with aiosqlite.connect('database.db') as db:
        async with httpx.AsyncClient() as client:

            if Code:
                ExchangedInfo = await AuthMethods.exchange_code(client, Code)
                if not ExchangedInfo[1]:
                    return "Invalid State"
                userinfo = await AuthMethods.get_user_info(client, ExchangedInfo[0]['access_token'])
                add_to_guild = await AuthMethods.add_to_guild(client, ExchangedInfo[0]['access_token'], userinfo['id'],
                                                              GuildID)
                if add_to_guild == 403:
                    return "You Are Banned From The Guild."
                response = make_response(f"Welcome To The Guild {userinfo['username']}#{userinfo['discriminator']}")
                FetchUserRow = await (
                    await db.execute('SELECT * FROM Members WHERE MainCode = ?', (userinfo['id'],))).fetchall()
                if len(FetchUserRow) == 0:
                    print("im fona set the cookie??")
                    response.set_cookie("Code", value=Code)
                    await db.execute('INSERT INTO Members VALUES(?,?,?,?, ?)', (
                        userinfo['id'], ExchangedInfo[0]['refresh_token'],
                        f"{userinfo['username']}#{userinfo['discriminator']}",
                        Code, False))
                else:
                    await db.execute('UPDATE Members SET RefreshToken = ? WHERE MemberID = ?',
                                     (ExchangedInfo[0]['refresh_token'],
                                      userinfo['id']))
                await db.commit()
                return response
            else:
                Cookie = request.cookies.get("Code")
                if Cookie:
                    fetch = await (await db.execute('SELECT * FROM Members WHERE MainCode = ?', (Cookie,))).fetchall()
                    print(fetch)
                    MemberID = fetch[0][0]
                    RefreshToken = fetch[0][1]
                    RefreshedInfo = await AuthMethods.refresh_token(client, RefreshToken)
                    if not RefreshedInfo[1]:
                        response = make_response("""<script>
                        window.onload = function () {
                            window.setTimeout(function () {
                                window.location.href = {}";
                            }, 5000)
                        };
                          </script>
                          <div>
                          Could Not Refresh your token, Will Redirect you after 5 seconds to reauthorize again
                          </div>""".format(RedirectURL))
                        response.delete_cookie("Code")
                        await db.execute('DELETE FROM Members WHERE MainCode = ?', Cookie)



                    access_token = RefreshedInfo[0]['access_token']
                    add_to_guild = await AuthMethods.add_to_guild(client, access_token, MemberID, GuildID)

                    if not add_to_guild:
                        return "Could not join you to the server" \
                               "It might be because you are banned or there's an issue with the system."

                    await db.execute('UPDATE Members SET RefreshToken = ? WHERE MemberID = ?',
                                     (RefreshedInfo[0]['refresh_token'], MemberID))
                    await db.commit()
                    return f"Welcome To The Guild {fetch[0][2]}"
                else:
                    return redirect(
                        RedirectURL,
                        302)


@app.route('/restore', methods=['POST'])
async def RestoreMembers():
    SecKey = request.get_json().get('SecretKey')

    if SecKey is not None and SecKey == SecretKey:
        async with aiosqlite.connect('database.db') as db:
            FetchAll = await (await db.execute('SELECT * FROM Members')).fetchall()
            async with httpx.AsyncClient() as client:
                for user in FetchAll:
                    userid = user[0]
                    RefreshToken = user[1]
                    RefreshedInfo = await AuthMethods.refresh_token(client, RefreshToken)
                    access_token = RefreshedInfo.get('access_token')
                    if access_token is None:
                        await db.execute('DELETE FROM Members WHERE MemberID = ?', (userid,))
                        continue
                    await db.execute('UPDATE Members SET RefreshToken = ? WHERE MemberID = ?',
                                     (RefreshedInfo[0]['refresh_token'], userid))
                    await AuthMethods.add_to_guild(client, access_token, userid, GuildID)
                return "Successfully Restored the members", 200
    return "Invalid Key", 401

app.run(debug=True)
