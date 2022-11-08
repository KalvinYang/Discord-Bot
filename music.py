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

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

        self.vc = None
        self.to_play = None

#Begin work on play function
#---------------------------------------

    def count_queue(self):
        count = 0
        for item in self.music_queue:
            count += 1
        return count

    @bot.command(pass_context=True)
    async def skip(self, ctx):
        await self.stop(ctx)
        self.next_song(ctx)

    @bot.command(pass_context=True)
    async def qlist(self, ctx):
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
        self.music_queue.append(song)
        print(self.music_queue)

    def next_song(self, ctx):
        time.sleep(3)
        try:
            song = self.music_queue.pop(0)
        except:
            self.is_playing = False
            return
        self.to_play.play(discord.FFmpegPCMAudio(song),
                          after=lambda e: self.next_song(ctx))
        return

    @bot.command(pass_context=True)
    async def play_music(self, ctx, url):
        await ctx.send("Playing song.")

        channel = ctx.author.voice
        ytdl = YoutubeDL(self.YDL_OPTIONS)
        holder = ytdl.extract_info(url, download=False)
        song = holder['url']
        await self.join(ctx)
        self.vc = channel.channel
        self.to_play = discord.utils.get(self.bot.voice_clients,
                                         guild=ctx.guild)

        self.is_playing = True
        self.to_play.play(discord.FFmpegPCMAudio(song),
                          after=lambda e: self.next_song(ctx))
        await self.autoleave(ctx)
        return

    @bot.command(pass_context=True)
    async def stop(self, ctx):
        self.to_play.stop()

    async def autoleave(self, ctx):
        while self.is_playing == True or self.is_paused == True:
            print('checking if playing')
            await asyncio.sleep(20)
        await self.disconnect(ctx)


#---------------------------------------

    @bot.command(pass_context=True)
    async def disconnect(self, ctx):
        #joins the discord vc
        channel = ctx.guild.voice_client
        self.vc = None
        await channel.disconnect()

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
