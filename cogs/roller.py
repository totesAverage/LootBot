import discord 
from discord.ext import commands
import os
import random

class roller(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['r'], help='LootBot will roll dice for you!')
  async def roll(self, ctx, dice: str):

    try:
      rolls, limit = map(int, dice.split('d'))

    except Exception:
      await ctx.send('Incorrect input. Please type in "NdN" format')
      return

    s = []

    for r in range(rolls):
      test = random.randint(1, limit)
      s.append(str(test))

    result = ', '.join(s)
    await ctx.send("You rolled: " + str(result))

def setup(client):
  client.add_cog(roller(client))
