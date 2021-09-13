import discord
from discord.ext import commands, tasks
import os

#Determines the acticity of the discord bot that is displayed
thing = discord.Activity(type=discord.ActivityType.listening, name="DnD!")

# Initialize the bot and set a command prefix
client = commands.Bot(command_prefix='#', activity=thing, status=discord.Status.online)

# Create extensions for the cogs to be loaded
@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

# Create extensions for the cogs to be unloaded
@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

# Load in the cogs 
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
    

client.run(os.getenv('lootbot_token'))
