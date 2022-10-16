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

    #Command allmembers, prints all members across all server that the bot is present in.
    @bot.command(pass_context=True)
    async def allmembers(self, ctx):
        for guild in self.bot.guilds:
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

    #Command clearbot, clears all messages from the bot within dms.
    @bot.command(pass_context=True)
    async def clearbot(self, ctx):
        dm = ctx.author.dm_channel
        bot_name = self.bot.user
        if dm != None:
            async for message in dm.history(limit=None):
                if message.author == bot_name:
                    await message.delete()
            await ctx.author.send("DMs deleted.")

    #Command clear, deletes all messages from a channel in one go.
    @bot.command(pass_context=True)
    async def clear(self, ctx):
        count = 0
        async for message in ctx.channel.history(limit=None):
            count += 1
        await ctx.channel.purge(limit=count)
        await ctx.send("All channel messages have been deleted.")

    #Command purge, deleting the number of messages dictated in field 'num'. 'All' used in command clear instead, 'my' replaced with targetted deletion. Limit of purge is 50, with the bot only being able to purge messages within the channel.
    @bot.command(pass_context=True)
    async def purge(self, ctx, num=0, id=""):
        counter = 0
        if num > 50:
            await ctx.send(
                'Too many messages to delete, please keep it under 50.')
            return
        elif num <= 0:
            await ctx.send('Choose a number greater than 0.')
            return
        if id == "":
            await ctx.channel.purge(limit=num)
        else:
            async for message in ctx.channel.history(limit=None):
                print('author: {0}'.format(str(message.author)))
                print('wanted: {0}'.format(id))
                if str(
                        message.author
                ) == id or message.author.name == id or message.author.mention == id:
                    counter += 1
                    await message.delete()
                    if counter == num:
                        return
            await ctx.channel.send("Messages deleted.")


def setup(bot):
    bot.add_cog(Private(bot))
