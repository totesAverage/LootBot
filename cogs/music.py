import discord
import os
import discordSuperUtils
from discord.ext import commands
from discordSuperUtils import MusicManager, PageManager

# Initialize the cog
class music(commands.Cog, discordSuperUtils.CogManager.Cog, name="music"):
    def __init__(self, bot):
      self.bot = bot
      self.client_secret = os.getenv('lootbot_secret')
      self.client_id = os.getenv('lootbot_id')
      # Client_secret and Client_id refer to your spotify developers ID and secret. If you wish to disable spotify, set spotify_support=False
      self.MusicManager = MusicManager(self.bot,client_id=self.client_id,client_secret=self.client_secret, spotify_support=True)
      super().__init__()
    

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_music_error(self, ctx, error):
      raise ValueError("LootBot doesn't understand!")
    
    # Displays the current music that is being played
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_play(self, ctx, player):
      await ctx.send(f"Now playing: {player}")

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx):
      print(f"The queue has ended in {ctx}")

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
      print(f"LootBot has left {ctx} due to inactivity..")

    
    @commands.command(aliases=['dc'], help='This command will disconnect LootBot from the voice channel')
    async def leave(self, ctx):
      if await self.MusicManager.leave(ctx):
        await ctx.send("LootBot has left the voice channel!")
      else:
        await ctx.send("LootBot isn't in the voice channel!")

    @commands.command(aliases=['j'], help='This command will make LootBot join the voice channel')
    async def join(self, ctx):
      if await self.MusicManager.join(ctx):
        await ctx.send('Joined the voice channel!')
      elif ctx.author.voice is None:
        await ctx.send('Please join the voice channel!')
      else:
        await ctx.send("You're already in the voice channel!")

    @commands.command(aliases=['p'], help='This command will make LootBot play music')
    async def play(self, ctx, *, query: str):
      await music.join(self, ctx)
      async with ctx.typing():
        player = await self.MusicManager.create_player(query)
      
      if player:
        await self.MusicManager.queue_add(players=player, ctx=ctx)

        if not await self.MusicManager.play(ctx):
          await ctx.send('Added to music queue!')
        
      else:
        await ctx.send("Sorry I can't find it")
    
    @commands.command(aliases=['stop'], help='This command will make LootBot stop playing music')
    async def pause(self, ctx):
      if await self.MusicManager.pause(ctx):
        await ctx.send('Paused! ⏸️')
      else:
        await ctx.send('No music is currently being played!')

    @commands.command(aliases=['continue'], help='This command will make LootBot resume music')
    async def resume(self, ctx):
      if await self.MusicManager.resume(ctx):
        await ctx.send('Resumed! ▶️')
      else:
        await ctx.send('LootBot is already resumed!')


    @commands.command(aliases=['v'], help='This command will let you control the volume of LootBot (Starts at 10)')
    async def volume(self, ctx, volume: int):
      if volume < 0:
        await ctx.send('Volume is too low!')
        return

      if volume > 150:
        await ctx.send('Volume is too high!')
        return
      
      
      await self.MusicManager.volume(ctx, volume)
      await ctx.send(f"Volume set to {volume}")


    @commands.command(aliases=['l'], help='This command will loop the music')
    async def loop(self, ctx):
      is_loop = await self.MusicManager.loop(ctx)
      await ctx.send(f"Looping is toggled to {is_loop}")

    @commands.command(aliases=['ql'], help='This command will loop the entire queue')
    async def queueloop(self,ctx):
      is_qloop = await self.MusicManager.queueloop(ctx)
      await ctx.send(f"Queue looping is toggled to {is_qloop}")

    @commands.command(aliases=['next'], help='This command will skip to the next item on the queue')
    async def skip(self, ctx, index: int= None):
      if self.MusicManager.skip(ctx, index):
        await ctx.send('Skipped! ⏭️')

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
