import sqlite3

import flask, aiosqlite, discord
from discord.ext import commands
from oAuthMethods import AuthMethods
from utils import UtilsObject
from flask import request, make_response, redirect
path = r'database.db'
app = flask.Flask(__name__, template_folder="html")
bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
connection = sqlite3.connect(path, check_same_thread=False)
db = connection.cursor()

@app.route('/join', methods=['GET'])
def MainRoute():

    Code = request.args.get('code')

    if Code:
      ExchangedInfo = AuthMethods.exchange_code(Code)
      if not ExchangedInfo[1]:
          return "Invalid State"
      userinfo = AuthMethods.get_user_info(ExchangedInfo[0]['access_token'])
      add_to_guild = AuthMethods.add_to_guild(ExchangedInfo[0]['access_token'], userinfo['id'], 1048851878546526238)
      if add_to_guild == 403:
          return "You Are Banned From The Guild."
      response = make_response(f"Welcome To The Guild {userinfo['username']}#{userinfo['discriminator']}")
      FetchUserRow = db.execute('SELECT * FROM Members WHERE MemberID = ?', (userinfo['id'],)).fetchall()
      if len(FetchUserRow) == 0:
           response.set_cookie("Code", value=Code)
           db.execute('INSERT INTO Members VALUES(?,?,?,?, ?)', (userinfo['id'], ExchangedInfo[0]['refresh_token'], f"{userinfo['username']}#{userinfo['discriminator']}",
                                                          Code, False))
      else:
           db.execute('UPDATE Members SET RefreshToken = ?, WHERE MemberID = ?', (ExchangedInfo[0]['refresh_token'],
                                                                                             userinfo['id']))
      connection.commit()
      return response
    else:
        Cookie = request.cookies.get("Code")
        if Cookie:
            fetch = db.execute('SELECT * FROM Members WHERE MainCode = ?', (Cookie,)).fetchall()
            print(fetch)
            MemberID = fetch[0][0]
            RefreshToken = fetch[0][1]
            RefreshedInfo = AuthMethods.refresh_token(RefreshToken)
            print(RefreshedInfo)
            access_token = RefreshedInfo['access_token']
            add_to_guild = AuthMethods.add_to_guild(access_token, MemberID, 1048851878546526238)
            if add_to_guild == 403:
                db.execute("DELETE FROM Members WHERE MemberID = ?", (MemberID,))
                resp = make_response("You Are Banned From The Guild.")
                resp.delete_cookie('Code')
                return resp
            db.execute('UPDATE Members SET RefreshToken = ? WHERE MemberID = ?',
                      (RefreshedInfo['refresh_token'], MemberID))
            connection.commit()
            return f"Welcome To The Guild {fetch[0][2]}"
        else:
            return redirect("https://discord.com/api/oauth2/authorize?client_id=1051888998504747078&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fjoin&response_type=code&scope=identify%20guilds.join", 302)



app.run(debug=True)
