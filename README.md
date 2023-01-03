# Discord-Member-Backup
This Project is used to backup and easily restore your members if your discord server ever gets nuked/deleted for any reason as well.
Download Python 3.10 or above to use this, You also need to host the flask application(main.py) on a vps/webserver, if you are too poor like me you can use https://pythonanywhere.com
Your bot needs to be in the server that you are going to add members to.
Steps:

- Create A Appliction in : https://discord.com/developers/applications and go to bot section and create a bot and enable all the intents bellow.
- Go to config.json and set all the required information.
- Create a oAuth URL with a redirect url for your webpage so it'll be like this : https://yourwebsite.com/join , and also select guild.join, identify.
- Now Run the main.py application on your vps or your webhost.
- Run the bot.py file to start the bot.
- Create a dummy server as a gateway to the main server and run this command in the channel: /SendAuthPanel
- Note The guildid in the config.json should be to the main server, not the gateway server.
- If you ever need to pull the members again or restore them in another server you can just change the guild id in config.json if it's another server and run this    command: /RestoreMembers

