import discord
import os
import discordSuperUtils
from discord.ext import commands
from discordSuperUtils import MusicManager, PageManager

# Initializes the cog
class music(commands.Cog, discordSuperUtils.CogManager.Cog, name="music"):
    
    def __init__(self, bot):
      self.bot = bot
      self.client_secret = os.getenv('lootbot_secret')
      self.client_id = os.getenv('lootbot_id')
      # Client id and Client secret refer to your spotify developer ID and secret. Enable spotify_support to true if you wish for the bot to be able to find spotify tracks.
      self.MusicManager = MusicManager(self.bot,client_id=self.client_id,client_secret=self.client_secret, spotify_support=True)
      super().__init__()

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_play(self, ctx, player):
      await ctx.send(f"Now playing: {player}", delete_after=15.0)

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx):
      print(f"The queue has ended in {ctx}")

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
      await music.clear(self, ctx)
      print(f"LootBot has left {ctx} due to inactivity..")

    
    @commands.command(aliases=['dc'], help='This command will disconnect LootBot from the voice channel')
    async def leave(self, ctx):
      if await self.MusicManager.leave(ctx):
        await music.clear(self, ctx)
        await ctx.send("LootBot has left the voice channel!", delete_after=10.0)
      else:
        await ctx.send("LootBot isn't in the voice channel!", delete_after=10.0)

    @commands.command(aliases=['j'], help='This command will make LootBot join the voice channel')
    async def join(self, ctx):
      if await self.MusicManager.join(ctx):
        await ctx.send('Joined the voice channel!', delete_after=10.0)
      elif ctx.author.voice is None:
        await ctx.send('Please join the voice channel!', delete_after=10.0)
      else:
        await ctx.send("You're already in the voice channel!", delete_after=10.0)

    @commands.command(aliases=['p'], help='This command will make LootBot play music')
    async def play(self, ctx, *, query: str):
      await music.join(self, ctx)
      async with ctx.typing():
        player = await self.MusicManager.create_player(query)
      
      if player:
        await self.MusicManager.queue_add(players=player, ctx=ctx)

        if not await self.MusicManager.play(ctx):
          await ctx.send('Added to music queue!', delete_after=5.0)
        
      else:
        await ctx.send("Sorry I can't find it", delete_after=20.0)
    
    @commands.command(aliases=['stop'], help='This command will make LootBot stop playing music')
    async def pause(self, ctx):
      if await self.MusicManager.pause(ctx):
        await ctx.send('Paused! ⏸️', delete_after=10.0)
      else:
        await ctx.send('No music is currently being played!', delete_after=10.0)

    @commands.command(aliases=['continue'], help='This command will make LootBot resume music')
    async def resume(self, ctx):
      if await self.MusicManager.resume(ctx):
        await ctx.send('Resumed! ▶️', delete_after=10.0)
      else:
        await ctx.send('LootBot is already resumed!', delete_after=5.0)


    @commands.command(aliases=['v'], help='This command will let you control the volume of LootBot (Starts at 10)')
    async def volume(self, ctx, volume: int):
      if volume < 0:
        await ctx.send('Volume is too low!')
        return

      if volume > 150:
        await ctx.send('Volume is too high!')
        return
      
      
      await self.MusicManager.volume(ctx, volume)
      await ctx.send(f"Volume set to {volume}", delete_after=10.0)


    @commands.command(aliases=['l'], help='This command will loop the music')
    async def loop(self, ctx):
      is_loop = await self.MusicManager.loop(ctx)
      await ctx.send(f"Looping is toggled to {is_loop}", delete_after=10.0)

    @commands.command(aliases=['ql'], help='This command will loop the entire queue')
    async def queueloop(self,ctx):
      is_qloop = await self.MusicManager.queueloop(ctx)
      await ctx.send(f"Queue looping is toggled to {is_qloop}", delete_after=10.0)

    @commands.command(aliases=['next'], help='This command will skip to the next item on the queue')
    async def skip(self, ctx, index: int= None):
      if await self.MusicManager.skip(ctx, index):
        await ctx.send('Skipped! ⏭️', delete_after=10.0)

    @commands.command(aliases=['c'], help='This clears the queue')
    async def clear(self, ctx):
      if await self.MusicManager.clear_queue(ctx):
        await ctx.send('Cleared! ', delete_after=10.0)

    @commands.command(help='Remove a song from the queue')
    async def remove(self, ctx, index: int):
      if await self.MusicManager.queue_remove(ctx, index):
        await ctx.send(f'{index} removed from queue!', delete_after=10.0)

    @commands.command(help='Displays the queue')
    async def queue(self,ctx):
      embeds = discordSuperUtils.generate_embeds(await self.MusicManager.get_queue(ctx),
         "Queue",
          f"Now Playing: {await self.MusicManager.now_playing(ctx)}",
          25,
          string_format="Title: {}")

      page_manager = PageManager(ctx, embeds, public=True)
      await page_manager.run()

    @commands.command(help='Displays the songs played')
    async def history(self, ctx):
      embeds = discordSuperUtils.generate_embeds(await self.MusicManager.history(ctx), "Song History", "Shows all played songs", 25, string_format="Title: {}")

      page_manager = PageManager(ctx, embeds, public=True)
      await page_manager.run()

def setup(client):
  client.add_cog(music(client))
