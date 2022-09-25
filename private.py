#Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands

#Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

#Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

#Command allmembers, originally called 'members' a piece of code taken and used to debug as to why the bot could only view itself when searching in guilds. It lists all users in every server that the bot is within, however list is only available within console.

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")

class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #private
    @bot.command(pass_context=True)
    async def allmembers(self, ctx):
        for guild in bot.guilds:
            for member in guild.members:
                print(guild, member)

    #Command members, a subset command of allmembers made into its' own that sends a list of all users in a server to the command caller.
    @bot.command(pass_context=True)
    async def members(self, ctx):
        the_guild = ctx.guild
        guild_members = ''
        count = 1
        for member in the_guild.members:
            guild_members = guild_members + str(
                count) + ': ' + member.name + '\n'
            count = count + 1
        await ctx.author.send(
            'List of guild members in {0}: \n'.format(the_guild) +
            guild_members)


def setup(bot):
    bot.add_cog(Private(bot))
