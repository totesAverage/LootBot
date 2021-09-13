import discord 
from discord.ext import commands
import os
import random

class roller(commands.Cog):

  # Initialize the cog
  def __init__(self, client):
    self.client = client

  # Rolls dice in NdN format  
  @commands.command(aliases=['r'], help='LootBot will roll dice for you!')
  async def roll(self, ctx, dice: str):

    # This will split the input into two integers, designating the first N to number of rolls and the second N to dice limit.
    try:
      rolls, limit = map(int, dice.split('d'))

    except Exception:
      await ctx.send('Incorrect input. Please type in "NdN" format')
      return
    
    # Create an empty array
    s = []

    # For the number of times of rolls, use randint to pick a number from 1 to the limit. It will only pick whole numbers. Put them in the empty list as strings.
    for r in range(rolls):
      test = random.randint(1, limit)
      s.append(str(test))

    # Join the results in the list together and store it to send
    result = ', '.join(s)
    await ctx.send("You rolled: " + str(result))

def setup(client):
  client.add_cog(roller(client))
