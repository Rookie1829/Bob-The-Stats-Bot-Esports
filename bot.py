import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('PANDASCORE_API_KEY')

intents = discord.Intents.default()
intents.messages = True  
intents.guilds = True    
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def fetch_data_from_pandascore(endpoint):
    """Utility function to fetch data from the PandaScore API."""
    url = f"https://api.pandascore.co/{endpoint}?token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@bot.command(name='help')
async def help(ctx):
    """Displays detailed help information for each command."""
    help_message = """
**Commands:**

- `!leagueinfo <game_slug> <league_slug>`: Displays info about a specific league.
- `!teamslist <game_slug>`: Lists all teams for a specified game.

**Game Slugs:**
- League of Legends: `lol`
- Dota 2: `dota2`
- CS:GO: `csgo`
- Valorant: `valorant`

**Usage Examples:**
- `!leagueinfo lol worlds` for League of Legends World Championship info.
- `!teamslist dota2` for listing Dota 2 teams.

Replace `<game_slug>` with one of the game slugs listed above, and `<league_slug>` with the league's slug for the `leagueinfo` command.
    """
    await ctx.send(help_message)

@bot.command(name='leagueinfo')
async def league_info(ctx, game_slug, league_slug):
    """Fetches and displays information about a specific league in a given game."""
    league_data = fetch_data_from_pandascore(f"{game_slug}/leagues?filter[slug]={league_slug}")
    if league_data:
        league = league_data[0]
        response_message = f"**League Name:** {league['name']}\n**League Image:** {league['image_url']}"
        await ctx.send(response_message)
    else:
        await ctx.send(f"Could not fetch league information for {game_slug} or league not found.")

@bot.command(name='teamslist')
async def teams_list(ctx, game_slug):
    """Lists all teams for a specified game."""
    teams_data = fetch_data_from_pandascore(f"{game_slug}/teams")
    if teams_data:
        response_message = f"**Teams in {game_slug}:**\n"
        for team in teams_data[:10]:  
            response_message += f"- {team['name']}\n"
        response_message += "Note: This is a limited list. Check the PandaScore website for more teams."
        await ctx.send(response_message)
    else:
        await ctx.send(f"Could not fetch teams for {game_slug} or game not found.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
