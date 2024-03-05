import requests
from discord.ext import commands
import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('PANDASCORE_API_KEY') 

intents = discord.Intents.default()
intents.messages = True 
intents.guilds = True  
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.command(name='help')
async def custom_help(ctx):
    help_message = """
Here are the commands you can use:
- `!help`: Shows this message.
- `!teamstats <game> <team_name>`: Shows statistics for a specific eSports team.
    """
    await ctx.send(help_message)

@bot.command(name='teamstats')
async def team_stats(ctx, game, team_name):
    """Fetches and displays statistics for a given eSports team."""
    url = f"https://api.pandascore.co/{game}/teams?search[name]={team_name}&token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        team_info = response.json()[0]
        response_message = f"Team: {team_info['name']}\nID: {team_info['id']}"
        await ctx.send(response_message)
    else:
        await ctx.send("Could not fetch team statistics or team not found.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
