import discord
from discord.ext import commands, tasks
import os

#random loot with dice 
thing = discord.Activity(type=discord.ActivityType.listening, name="DnD!")

client = commands.Bot(command_prefix='#', activity=thing, status=discord.Status.online)

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
    

client.run(os.getenv('lootbot_token'))
