import discord
import asyncio
import time
from discord.ext import commands
from youtube_dl import YoutubeDL

#Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

#Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.titles = []
        self.current_song = ""

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

        self.vc = None
        self.to_play = None

#Non-command functions
#---------------------------------------

    def count_queue(self):
        count = 0
        for item in self.music_queue:
            count += 1
        return count

    def next_song(self, ctx):
        try:
            song = self.music_queue.pop(0)
            self.current_song = self.titles.pop(0)
        except:
            self.is_playing = False
            self.current_song = ""
            return
        self.to_play.play(discord.FFmpegPCMAudio(song),
                          after=lambda e: self.next_song(ctx))
        return

    async def autoleave(self, ctx):
        while self.is_playing == True or self.is_paused == True:
            await asyncio.sleep(20)
        if self.vc == None:
          return
        self.resetvoice()
        await self.disconnect(ctx)

    def speakingnow(self, ctx):
        if not self.is_paused and not self.is_playing:
            return False
        return True

    def resetvoice(self):
      self.vc = None
      self.to_play = None

#---------------------------------------

    @bot.command(pass_context=True)
    async def skip(self, ctx):
        self.to_play.stop()

    @bot.command(pass_context=True)
    async def c_song(self, ctx):
        await ctx.send("Current song: " + self.current_song)

    @bot.command(pass_context=True)
    async def qlist(self, ctx):
        the_list = "Current song: " + self.current_song + "\n"
        count = 0
        for i in self.titles:
            count = count + 1
            the_list = the_list + str(count) + ": " + i + '\n'
        await ctx.send(the_list)

    @bot.command(pass_context=True)
    async def qlength(self, ctx):
        count = 0
        if self.music_queue == False:
            await ctx.send('No items in queue.')
        count = self.count_queue()
        if count == 1:
            await ctx.send(str(count + 'item in queue.'))
            return
        await ctx.send(str(count) + ' items in queue.')

    @bot.command(pass_context=True)
    async def queue(self, ctx, url):
        ytdl = YoutubeDL(self.YDL_OPTIONS)
        holder = ytdl.extract_info(url, download=False)
        song = holder['url']
        self.titles.append(holder.get('title'))
        self.music_queue.append(song)
        print(self.titles)

    @bot.command(pass_context=True)
    async def play_q(self,ctx):
      if self.vc == None:
        await self.join(ctx)
      self.to_play = discord.utils.get(self.bot.voice_clients,
                                           guild=ctx.guild)
      self.next_song(ctx)
  
    @bot.command(pass_context=True)
    async def play_music(self, ctx, url):
    
        await self.queue(ctx, url)
      
        if self.speakingnow(ctx):
          await ctx.send("There is a song playing already, queued song instead.")
        else:
          self.current_song = self.titles.pop(-1)
          song = self.music_queue.pop(-1) 

          if self.vc == None:
            await self.join(ctx)
          self.to_play = discord.utils.get(self.bot.voice_clients,
                                           guild=ctx.guild)
  
          self.is_playing = True
          self.to_play.play(discord.FFmpegPCMAudio(song),
                            after=lambda e: self.next_song(ctx))
          
          await ctx.send("Playing video.")
          await self.autoleave(ctx)

    @bot.command(pass_context=True)
    async def pause(self, ctx):
        if not self.speakingnow(ctx):
            await ctx.send("Not playing anything.")
            return
        elif self.is_paused:
            await ctx.send("Already paused.")
        else:
            self.to_play.pause()
            self.is_paused = True
            self.is_playing = False

    @bot.command(pass_context=True)
    async def resume(self, ctx):
        if not self.speakingnow(ctx):
            await ctx.send("Not playing anything.")
            return
        elif self.is_playing:
            await ctx.send("Already playing.")
        else:
            self.to_play.resume()
            self.is_playing = True
            self.is_paused = False

    @bot.command(pass_context=True)
    async def clear_q(self):
        self.music_queue.clear()
        self.titles.clear()
  
    @bot.command(pass_context=True)
    async def stop(self, ctx):
        await self.clear_q()
        self.current_song = ""
        await self.skip(ctx)

    @bot.command(pass_context=True)
    async def disconnect(self, ctx):
        if self.count_queue() > 0 or not self.current_song == "":
          await self.stop(ctx)
        channel = ctx.guild.voice_client
        await channel.disconnect()
        self.resetvoice()

    #Command Join, Allows the Roomz Bot to join a voice channel from where the user is already in when the command is called
    @bot.command(pass_context=True)
    async def join(self, ctx):

        if ctx.author.voice == None:
            await ctx.send("You aren't in a channel.")
            return

        #joins the discord vc
        channel = ctx.author.voice.channel

        if self.vc == None:
            await channel.connect()

        elif not discord.utils.get(self.bot.voice_clients,
                                   guild=ctx.guild).channel == channel:
            await self.disconnect
            await channel.connect()

        else:
            await ctx.send('I am already here!')

        self.vc = channel


def setup(bot):
    bot.add_cog(Music(bot))
