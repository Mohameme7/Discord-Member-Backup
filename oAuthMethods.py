
from utils import *
Config = LoadJson()
ClientID = Config['ClientID']
ClientSecret = Config['ClientSecret']
BotToken = Config['BotToken']
APIEndpoint = Config['APIEndpoint']
GuildID = Config['GuildID']

class AuthMethods:
    @staticmethod
    async def exchange_code(Client, code):
        data = {
            'client_id': ClientID,
            'client_secret': ClientSecret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': "http://127.0.0.1:5000/join"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = await Client.post('%s/oauth2/token' % APIEndpoint, data=data, headers=headers)
        return (r.json()), r.is_success

    @staticmethod
    async def add_to_guild(Client, access_token, userID, guildID):
        url = f"{APIEndpoint}/guilds/{guildID}/members/{userID}"
        data = {
            "access_token": access_token,
        }
        headers = {
            "Authorization": f"Bot {BotToken}",
            'Content-Type': 'application/json'
        }
        request = await Client.put(url=url, headers=headers, json=data)
        return request.is_success

    @staticmethod
    async def refresh_token(Client, refresh_token):
        data = {
            'client_id': ClientID,
            'client_secret': ClientSecret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = await Client.post('%s/oauth2/token' % APIEndpoint, data=data, headers=headers)
        return r.json(), r.is_success

    @staticmethod
    async def get_user_info(Client, Access_Token):
        request = await Client.get('https://discord.com/api/v9/users/@me', headers={"Authorization": f"Bearer {Access_Token}"})
        return request.json()
