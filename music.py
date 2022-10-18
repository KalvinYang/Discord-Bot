import discord
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

#Begin work on play function
#---------------------------------------

    @bot.command(pass_context=True)
    async def play(self, ctx, *args):
        return


#---------------------------------------

    @bot.command(pass_context=True)
    async def disconnect(self, ctx):
        #joins the discord vc
        channel = ctx.guild.voice_client
        await channel.disconnect()

    #Command Join, Allows the Roomz Bot to join a voice channel from where the user is already in when the command is called
    @bot.command(pass_context=True)
    async def join(self, ctx):
        #joins the discord vc
        channel = ctx.author.voice.channel
        connected = ctx.guild.voice_client
        try:
            await channel.connect()
        except discord.ClientException:
            voice_client = discord.utils.get(
                self.bot.voice_clients, guild=ctx.guild
            )  #gets bot channel object, need the channel by using .channel
            if channel == voice_client.channel:
                await ctx.send('I am already here!')
            else:
                await connected.disconnect()
                await channel.connect()


def setup(bot):
    bot.add_cog(Music(bot))
