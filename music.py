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
        self.durations = []

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True,
'forceduration':True}

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

    def samechannel(self, ctx):
      if self.vc == ctx.author.voice.channel:
        return True
      return False


#---------------------------------------

    @bot.command(pass_context=True,
                 aliases=["sk", "next", "n"],
                 brief="Skips current song.",
                 description="If the bot is playing music with a queue it will skip the current song and switch to the next song in queue. If no other song is in queue, there will be no sound. Will not work in you are not in the same channel as the bot.\n\n**Usage:**\n&skip")
    async def skip(self, ctx):
        if self.samechannel(ctx):
          self.to_play.stop()

    @bot.command(pass_context=True,
                 aliases=["cs", "csong", "current", "playing"],
                 brief="Says current song.",
                 description="If there is a current song it will say the title of it.\n\n**Usage:**\n&current_song")
    async def current_song(self, ctx):
        await ctx.send("Current song: " + self.current_song)

    @bot.command(pass_context=True,
                 aliases=["allqueued","qli","al"],
                 brief="Shows all queued songs.",
                 description="Shows all song titles in queue and the playlist order.\n\n**Usage:**\n&qlist")
    async def qlist(self, ctx):
        the_list = "Current song: " + self.current_song + "\n"
        count = 0
        for i in self.titles:
            count = count + 1
            the_list = the_list + str(count) + ": " + i + '\n'
        await ctx.send(the_list)

    @bot.command(pass_context=True,
                 aliases=["qle","qlen"],
                 brief="Says queue length.",
                 description="Sends the length of the queue.\n\n**Usage:**\n&qlength")
    async def qlength(self, ctx):
        count = 0
        if self.music_queue == False:
            await ctx.send('No items in queue.')
        count = self.count_queue()
        if count == 1:
            await ctx.send(str(count + 'item in queue.'))
            return
        await ctx.send(str(count) + ' items in queue.')

    @bot.command(pass_context=True,
                 aliases=["q","qup"],
                 brief="Queues up a song.",
                 description="Given a youtube link to a video, adds the song to the current queue.\n\n**Usage:**\n&queue {link}")
    async def queue(self, ctx, url):
      if self.samechannel(ctx):
          ytdl = YoutubeDL(self.YDL_OPTIONS)
          holder = ytdl.extract_info(url, download=False)
          song = holder['url']
          self.titles.append(holder.get('title'))
          self.music_queue.append(song)
          print(self.titles)

    @bot.command(pass_context=True,
                 aliases=["pq","playq"],
                 brief="Plays music from queue.",
                 description="From queue, play music if queue has any items. If music is already playing nothing will happen.\n\n**Usage:**\n&play_q")
    async def play_q(self, ctx):
      if self.samechannel(ctx):
          if self.speakingnow(ctx):
            self.is_playing=True
            if self.vc == None:
                await self.join(ctx)
            self.to_play = discord.utils.get(self.bot.voice_clients,
                                             guild=ctx.guild)
            self.next_song(ctx)
          else:
            await ctx.send("Currently playing something, or something is paused.")
          await self.autoleave(ctx)

    @bot.command(pass_context=True,
                 aliases=["playmusic","playm","play"],
                 brief="Plays specified song.",
                 description="Given a youtube link, play the specified song. If the bot is not already in user's call, it will join the call then play music. If there is already queued music, but no audio is currently playing, then given link will play first and then start playing the queue. If a song is already playing, then the link will be queued instead.\n\n**Usage:**\n&play_music {link}")
    async def play_music(self, ctx, url):

        if self.vc == None:
                  await self.join(ctx)

        await self.queue(ctx, url)

        if self.speakingnow(ctx):
            await ctx.send(
                "There is a song playing already, queued song instead.")
        else:
            self.current_song = self.titles.pop(-1)
            song = self.music_queue.pop(-1)

            self.to_play = discord.utils.get(self.bot.voice_clients,
                                             guild=ctx.guild)

            self.is_playing = True
            self.to_play.play(discord.FFmpegPCMAudio(song),
                              after=lambda e: self.next_song(ctx))

            await ctx.send("Playing video.")
            await self.autoleave(ctx)

    @bot.command(pass_context=True,
                 aliases=["ff"],
                 brief="Seek forward or back some number of seconds.",
                 description="holder 69") #Remember to make a description, use other commands as a reference.
    async def seek(self, ctx):
      #figure out a way to get the timestamp using youtubeDL, should be similar to how queue loads information. time_arg should be in the form of a string as they would seek something along the lines of min:seconds, which we can then convert to seconds and find such information in youtubeDL's loaded info. then, we check if it is valid and play the song at that point (second hard part)
      if self.speakingnow(ctx):
        url = self.music_queue[0]
        ytdl = YoutubeDL(self.YDL_OPTIONS)
        holder = ytdl.extract_info(url, download=False)
        dur = holder['duration']
        print(dur)
        return
      await ctx.send("nothing playing, invalid seek")
      
      return
      
    @bot.command(pass_context=True,
                 aliases=["pa",'p'],
                 brief="Pauses audio.",
                 description="If the bot is in the same channel as the user and is currently playing audio it will pause said audio. Otherwise this command does nothing.\n\n**Usage:**\n&pause")
    async def pause(self, ctx):
      if self.samechannel(ctx):
          if not self.speakingnow(ctx):
              await ctx.send("Not playing anything.")
              return
          elif self.is_paused:
              await ctx.send("Already paused.")
          else:
              self.to_play.pause()
              self.is_paused = True
              self.is_playing = False

    @bot.command(pass_context=True,
                 aliases=["re","continue"],
                 brief="Plays paused audio.",
                 description="If the bot is in the same channel as the user and is currently paused it will continue playing the audio. Otherwise this command does nothing.\n\n**Usage:**\n&resume")
    async def resume(self, ctx):
      if self.samechannel(ctx):
          if not self.speakingnow(ctx):
              await ctx.send("Not playing anything.")
              return
          elif self.is_playing:
              await ctx.send("Already playing.")
          else:
              self.to_play.resume()
              self.is_playing = True
              self.is_paused = False

    @bot.command(pass_context=True,
                 aliases=["clearq","clq"],
                 brief="Clears queue.",
                 description="Clears all items from the current queue.\n\n**Usage:**\n&clear_q")
    async def clear_q(self, ctx):
      if self.samechannel(ctx):
          self.music_queue.clear()
          self.titles.clear()

    @bot.command(pass_context=True,
                 aliases=["st"],
                 brief="Clears queue and stops audio.",
                 description="Clears all items from the current queue and stops playing current audio.\n\n**Usage:**\n&stop")
    async def stop(self, ctx):
      if self.samechannel(ctx):
          await self.clear_q(ctx)
          self.current_song = ""
          await self.skip(ctx)

    @bot.command(pass_context=True,
                 aliases=["countqueue","countq","cqueue","cq"],
                 brief="Diconnect bot from channel.",
                 description="If the bot is in the user's channel, it will clear queue and stop current song and then leave the voice channel.\n\n**Usage:**\n&disconnect")
    async def disconnect(self, ctx):
        if self.count_queue() > 0 or not self.current_song == "":
            await self.stop(ctx)
        channel = ctx.guild.voice_client
        await channel.disconnect()
        self.resetvoice()

    #Command Join, Allows the Roomz Bot to join a voice channel from where the user is already in when the command is called
    @bot.command(pass_context=True,
                 aliases=['j'],
                 brief="Join the user's voice channel.",
                 description="If the user is in a voice channel, the bot will join that channel. It will say that it is already there if in the same channel already.\n\n**Usage:**\n&join")
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
