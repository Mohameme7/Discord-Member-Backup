import json
import sys
import httpx
from colorama import Fore
from utils import UtilsObject
Config = UtilsObject.LoadJson()
ClientID = Config['ClientID']
ClientSecret = Config['ClientSecret']
BotToken = Config['BotToken']
APIEndpoint = Config['APIEndpoint']


class AuthMethods:
    @staticmethod
    def exchange_code(code):
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
        r = httpx.post('%s/oauth2/token' % APIEndpoint, data=data, headers=headers)
        print(r.json())
        return (r.json(), r.is_success)

    @staticmethod
    def add_to_guild(access_token, userID, guildID):
        url = f"{APIEndpoint}/guilds/{guildID}/members/{userID}"
        data = {
            "access_token": access_token,
        }
        headers = {
            "Authorization": f"Bot {BotToken}",
            'Content-Type': 'application/json'
        }
        response = httpx.put(url=url, headers=headers, json=data)
        return response.status_code

    @staticmethod
    def refresh_token(refresh_token):
        data = {
            'client_id': ClientID,
            'client_secret': ClientSecret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = httpx.post('%s/oauth2/token' % APIEndpoint, data=data, headers=headers)
        print(r.json(), "refdsads")
        return r.json()

    @staticmethod
    def get_user_info(Access_Token):
        request = httpx.get('https://discord.com/api/v9/users/@me', headers={"Authorization": f"Bearer {Access_Token}"})
        print(request.json())
        return request.json()