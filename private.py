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
      
    #work in progress, don't tinker with this please.
    @bot.command(pass_context=True)
    async def clearbot(self, ctx):
        dm = ctx.author.dm_channel
        await ctx.author.send("Initiating deletion of dms.")
        bot_name = "Roomz Bot#9241"
        if dm != None:
            await ctx.author.send("Getting there.")
            async for message in dm.history(limit=None):
                print('author: {0}'.format(
                    message.author))
                print('   bot: {0} \n'.format(bot_name))
                print('message: {0}\n'.format(message))
                holder = message
                if message.author == bot_name:
                    print('message deleted.')
                    await holder.delete()
            await ctx.author.send("DMs deleted.")

    #Command clear, deletes all messages from a channel in one go.
    @bot.command(pass_context=True)
    async def clear(self, ctx):
        await ctx.author.send(
            "Deleting all messages, beware any messages from here on will be deleted."
        )
        count = 0
        async for message in ctx.channel.history(limit=None):
            count += 1
        await ctx.channel.purge(limit=count)
        await ctx.send("All channel messages have been deleted.")

    #Command purge, deleting the number of messages dictated in field 'num'. 'num' must also be convertible to type int or else the command will not work. Thinking of working on changing this fact, by adding keywords like 'all' or 'my' with a third redundant field that only works when the other keywords are in effect.
    @bot.command(pass_context=True)
    async def purge(self, ctx, num):
        num = int(num)
        if num > 50:
            await ctx.send(
                'Too many messages to delete, please keep it under 50.')
            return
        await ctx.channel.purge(limit=num)


def setup(bot):
    bot.add_cog(Private(bot))
