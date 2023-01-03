import discord
import requests
from discord.ext import commands
from utils import *

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
Config = LoadJson()
BotToken = Config['BotToken']
RedirectURL = Config['oAuthURL']
OwnerID = Config['OwnerID']
Secretkey = Config['SecretKey']


@bot.event
async def on_ready():
    log(f"Ready To Go! {bot.user}")


@bot.tree.command()
@commands.has_permissions(administrator=True)
async def SendAuthPanel(interaction: discord.Interaction):
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style=style, label="Read the docs!",
                             url=RedirectURL)
    view.add_item(item=item)
    await interaction.response.send_message(
        embed=discord.Embed(title="Server Verification", description="Please Verify by clicking on the button bellow,"),
        view=view)


@bot.tree.command()
async def RestoreMembers(interaction: discord.Interaction):
    if interaction.user.id == OwnerID:
        requests.post('http://127.0.0.1:5000/restore', json={"SecretKey": Secretkey})
        await interaction.response.send_message("Restoring Members Now", ephemeral=True)
    else:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)


bot.run(BotToken)
