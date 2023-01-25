#Imports
import discord
import asyncio
import time
import datetime
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
    #Class variables used throughout functions and commands
    def __init__(self, bot):
        self.bot = bot

        #Checks for if audio is still going, or stopped
        self.is_playing = False
        self.is_paused = False

        #Song based variables
        self.music_queue = []
        self.titles = []
        self.current_song = ""
        self.durations = []

        #Youtubedl settings
        self.YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': True,
            'forceduration': True
        }

        #Channel location
        self.vc = None
        self.to_play = None

        self.ecolor = 0x9b59b6
#Non-command functions
#---------------------------------------

    #Using music_queue cog variable count how many songs are in queue
    def count_queue(self):
        count = len(self.music_queue)
        return count

    #Automatically plays the next song
    def next_song(self, ctx):
        try:
            #try to take from the music queue
            song = self.music_queue.pop(0)
            self.current_song = self.titles.pop(0)
        except:
            #If nothing there set the checks to base case and return
            self.is_playing = False
            self.current_song = ""
            return
        #Play music while recursive call when song ends
        self.to_play.play(discord.FFmpegPCMAudio(song),
                          after=lambda e: self.next_song(ctx))
        return

    #Makes the bot leave the voice channel if checks are false after a short amount of time
    async def autoleave(self, ctx):
        #If checks true, wait
        while self.is_playing == True or self.is_paused == True:
            await asyncio.sleep(20)
        #If not in voice channel, do nothing
        if self.vc == None:
            return
        #Otherwise reset voice channel variables, then leave channel
        self.resetvoice()
        await self.disconnect(ctx)

    #If checks both false, return false, otherwise true
    def speakingnow(self, ctx):
        if not self.is_paused and not self.is_playing:
            return False
        return True

    #Resets cog voice channel variables
    def resetvoice(self):
        self.vc = None
        self.to_play = None

    #True if user in bot channel, false otherwise
    def samechannel(self, ctx):
        if self.vc == ctx.author.voice.channel:
            return True
        return False

    #
    #Embedding for message ui looking better, automatically set to sending to origin channel
    async def embed(self, ctx, message="", sendto=1, user=None):
        #Take cog color (self.ecolor) as color, and command name as title
        emb = discord.Embed(color=self.ecolor,
                            title=str(ctx.command).capitalize() + " Results:")
        #Sets the user that called command as author by taking their name and pfp
        emb.set_author(name=ctx.author.display_name,
                       url=discord.embeds.EmptyEmbed,
                       icon_url=ctx.author.avatar_url)
        #Set message of embed
        emb.description = message
        #Send to origin channel
        if sendto==1:
          await ctx.send(embed=emb)
        #Send to user direct messages
        elif sendto==2:
          await ctx.author.send(embed=emb)
        #Send to origin channel alternate
        elif sendto==3:
          await ctx.channel.send(embed=emb)
        #Send to specified user
        elif sendto==4 and not user ==None:
          try:
            await user.send(embed=emb)
          except:
            #If no such user, send back command fail
            emb.description = "An error occurred."
            await ctx.author.send(embed=emb)

#---------------------------------------

    @bot.command(
        pass_context=True,
        aliases=["sk", "next", "n"],
        brief="Skips current song.",
        description=
        "If the bot is playing music with a queue it will skip the current song and switch to the next song in queue. If no other song is in queue, there will be no sound. Will not work in you are not in the same channel as the bot.\n\n**Usage:**\n&skip"
    )
    async def skip(self, ctx):
        if self.samechannel(ctx):
            self.to_play.stop()
            await self.embed(ctx,"Skipped song.")

    @bot.command(
        pass_context=True,
        aliases=["cs", "csong", "current", "playing"],
        brief="Says current song.",
        description=
        "If there is a current song it will say the title of it.\n\n**Usage:**\n&current_song"
    )
    async def current_song(self, ctx):
        await self.embed(ctx, "Current song: " + self.current_song)

    @bot.command(
        pass_context=True,
        aliases=["allqueued", "qli", "al"],
        brief="Shows all queued songs.",
        description=
        "Shows all song titles in queue and the playlist order.\n\n**Usage:**\n&qlist"
    )
    async def qlist(self, ctx):
        the_list = "**Current song:** " + self.current_song + "\n\n"
        count = 0
        for i in self.titles:
            count = count + 1
            the_list = the_list + "**" + str(count) + ":** " + i + '\n'
        await self.embed(ctx, the_list)

    @bot.command(
        pass_context=True,
        aliases=["qle", "qlen"],
        brief="Says queue length.",
        description="Sends the length of the queue.\n\n**Usage:**\n&qlength")
    async def qlength(self, ctx):
        count = 0
        count = self.count_queue()
        if count == 1:
            await self.embed(ctx, str(count + 'item in queue.'))
        else:
            await self.embed(ctx, str(count) + ' items in queue.')

    @bot.command(
        pass_context=True,
        aliases=["q", "qup"],
        brief="Queues up a song.",
        description=
        "Given a youtube link to a video, adds the song to the current queue.\n\n**Usage:**\n&queue {link}"
    )
    async def queue(self, ctx, url):
        if self.samechannel(ctx):
            ytdl = YoutubeDL(self.YDL_OPTIONS)
            holder = ytdl.extract_info(url, download=False)
            song = holder['url']
            self.titles.append(holder.get('title'))
            self.music_queue.append(song)
            print(self.titles)
            await self.embed(ctx, "Your song has been queued.")

    @bot.command(
        pass_context=True,
        aliases=["pq", "playq"],
        brief="Plays music from queue.",
        description=
        "From queue, play music if queue has any items. If music is already playing nothing will happen.\n\n**Usage:**\n&play_q"
    )
    async def play_q(self, ctx):
        if self.samechannel(ctx):
            if self.speakingnow(ctx):
                self.is_playing = True
                if self.vc == None:
                    await self.join(ctx)
                self.to_play = discord.utils.get(self.bot.voice_clients,
                                                 guild=ctx.guild)
                self.next_song(ctx)
            else:
                await self.embed(
                    ctx,
                    "Currently playing something, or something is paused.")
            await self.autoleave(ctx)

    @bot.command(
        pass_context=True,
        aliases=["playmusic", "playm", "play"],
        brief="Plays specified song.",
        description=
        "Given a youtube link, play the specified song. If the bot is not already in user's call, it will join the call then play music. If there is already queued music, but no audio is currently playing, then given link will play first and then start playing the queue. If a song is already playing, then the link will be queued instead.\n\n**Usage:**\n&play_music {link}"
    )
    async def play_music(self, ctx, url):

        if self.vc == None:
            await self.join(ctx)

        await self.queue(ctx, url)

        if self.speakingnow(ctx):
            await self.embed(
                ctx, "There is a song playing already, queuing song instead.")
        else:
            self.current_song = self.titles.pop(-1)
            song = self.music_queue.pop(-1)

            self.to_play = discord.utils.get(self.bot.voice_clients,
                                             guild=ctx.guild)

            self.is_playing = True
            self.to_play.play(discord.FFmpegPCMAudio(song),
                              after=lambda e: self.next_song(ctx))
            await self.embed(ctx, "Playing now.")
            await self.autoleave(ctx)

    @bot.command(
        pass_context=True,
        aliases=["ff"],
        brief="Seek forward or back some number of seconds.",
        description="holder 69"
    )  #Remember to make a description, use other commands as a reference.
    async def seek(self, ctx, timestamp):
        #figure out a way to get the timestamp using youtubeDL, should be similar to how queue loads information. time_arg should be in the form of a string as they would seek something along the lines of min:seconds, which we can then convert to seconds and find such information in youtubeDL's loaded info. then, we check if it is valid and play the song at that point (second hard part)
        if self.speakingnow(ctx):
            url = self.music_queue[0]
            ytdl = YoutubeDL(self.YDL_OPTIONS)
            holder = ytdl.extract_info(url, download=False)
            dur = holder['duration']
            print(dur)
            timestamp = 0
            return
        await ctx.send(
            "nothing playing, invalid seek"
        )  #Switching to embeds, heads up for you to change later.

        return

    @bot.command(
        pass_context=True,
        aliases=["pa", 'p'],
        brief="Pauses audio.",
        description=
        "If the bot is in the same channel as the user and is currently playing audio it will pause said audio. Otherwise this command does nothing.\n\n**Usage:**\n&pause"
    )
    async def pause(self, ctx):
        if self.samechannel(ctx):
            if not self.speakingnow(ctx):
                await self.embed(ctx,"Not playing anything.")
                return
            elif self.is_paused:
                await self.embed(ctx,"Already paused.")
            else:
                self.to_play.pause()
                self.is_paused = True
                self.is_playing = False
                await self.embed(ctx,"Paused.")

    @bot.command(
        pass_context=True,
        aliases=["re", "continue"],
        brief="Plays paused audio.",
        description=
        "If the bot is in the same channel as the user and is currently paused it will continue playing the audio. Otherwise this command does nothing.\n\n**Usage:**\n&resume"
    )
    async def resume(self, ctx):
        if self.samechannel(ctx):
            if not self.speakingnow(ctx):
                await self.embed(ctx,"Not playing anything.")
                return
            elif self.is_playing:
                await self.embed(ctx,"Already playing.")
            else:
                self.to_play.resume()
                self.is_playing = True
                self.is_paused = False
                await self.embed(ctx,"Resumed.")

    @bot.command(
        pass_context=True,
        aliases=["clearq", "clq"],
        brief="Clears queue.",
        description=
        "Clears all items from the current queue.\n\n**Usage:**\n&clear_q")
    async def clear_q(self, ctx):
        if self.samechannel(ctx):
            self.music_queue.clear()
            self.titles.clear()
            await self.embed(ctx,"Queue cleared.")

    @bot.command(
        pass_context=True,
        aliases=["st"],
        brief="Clears queue and stops audio.",
        description=
        "Clears all items from the current queue and stops playing current audio.\n\n**Usage:**\n&stop"
    )
    async def stop(self, ctx):
        if self.samechannel(ctx):
            await self.clear_q(ctx)
            self.current_song = ""
            await self.skip(ctx)
            await self.embed(ctx,"Stopped.")

    @bot.command(
        pass_context=True,
        aliases=["countqueue", "countq", "cqueue", "cq"],
        brief="Diconnect bot from channel.",
        description=
        "If the bot is in the user's channel, it will clear queue and stop current song and then leave the voice channel.\n\n**Usage:**\n&disconnect"
    )
    async def disconnect(self, ctx):
        if self.count_queue() > 0 or not self.current_song == "":
            await self.stop(ctx)
        channel = ctx.guild.voice_client
        await channel.disconnect()
        self.resetvoice()
        await self.embed(ctx,"Disconnected.")

    #Command Join, Allows the Roomz Bot to join a voice channel from where the user is already in when the command is called
    @bot.command(
        pass_context=True,
        aliases=['j'],
        brief="Join the user's voice channel.",
        description=
        "If the user is in a voice channel, the bot will join that channel. It will say that it is already there if in the same channel already.\n\n**Usage:**\n&join"
    )
    async def join(self, ctx):

        if ctx.author.voice == None:
            await self.embed(ctx,"You aren't in a channel.")
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
            await self.embed(ctx,'I am already here!')

        self.vc = channel


async def setup(bot):
    await bot.add_cog(Music(bot))
