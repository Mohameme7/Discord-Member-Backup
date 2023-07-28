# Discord Member Backup
This project is capable of restoring your server members if your server gets nuked/banned.

## How to set up
Download Python 3.10 or above to use this, You also need to host the flask application(main.py) on a vps/webserver, if you are too poor like me you can use https://pythonanywhere.com
Your bot needs to be in the server that you are going to add members to.
Steps:

- Create a bot in https://discord.com/developers/applications and then enable all intents
- Go to `config.json` and set all the required information.
- Create a oAuth URL with a redirect url for your webpage so it'll be like this: https://yourwebsite.com/join, and also select guild.join, identify.
- Now Run the main.py application on your vps or your webhost.
- Run the bot.py file to start the bot.
- Create a dummy server as a gateway to the main server and run this command in the channel: /SendAuthPanel
- Note The guildid in the config.json should be to the main server, not the gateway server.

## Note
If you ever need to pull the members again or restore them in another server you can just change the Guild ID in config.json, and run this command: `/RestoreMembers`
You'll also need to setup up a deployment sever and change things in code, here's a guide for that https://flask.palletsprojects.com/en/2.3.x/deploying/
