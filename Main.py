import discord
from discord.ext import commands, tasks
import os
import random

#random loot with dice 
client = commands.Bot(command_prefix='/')

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = 'Hello World!'
    await ctx.send(responses)

# Rolls dice in NdN format
@client.command(aliases=['r'])
async def roll(ctx, dice: str):
  # gets the number of rolls (first N) and the dice type (second N)
  # and stores them in two separate values. Map function applies the int function without needing a loop
    try:
        rolls, limit = map(int, dice.split('d'))
    # To prevent any format other than NdN
    except Exception:
        await ctx.send('Incorrect input. Please type in "NdN" format')
        return

    s = []
    # For the number of rolls, the for loop will add a number to the empty list as a string
    for r in range(rolls):
      test = random.randint(1, limit)
      s.append(str(test))
    # joins all the strings in the list with a , between them
    result = ', '.join(s)
    await ctx.send("You rolled: " + str(result))


client.run(os.getenv('lootbot_token'))