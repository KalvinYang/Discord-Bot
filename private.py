# Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands
import asyncio

# Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

# Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

# Command allmembers, originally called 'members' a piece of code taken and used to debug as to why the bot could
# only view itself when searching in guilds. It lists all users in every server that the bot is within, however list
# is only available within console.

# Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")


class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ecolor = 0x992d22

        # Embedding for message ui looking better, automatically set to sending to origin channel

    async def embed(self, ctx, message="", sendto=1, user=None, bot_level=""):
        # Take cog color (self.ecolor) as color, and command name as title
        if bot_level == "":
            emb = discord.Embed(color=self.ecolor,
                                title=str(ctx.command).capitalize() + " Results:")
        else:
            emb = discord.Embed(color=self.ecolor,
                                title=bot_level)
        # Sets the user that called command as author by taking their name and pfp
        emb.set_author(name=ctx.author.display_name,
                       icon_url=ctx.author.avatar)
        # Set message of embed
        emb.description = message
        # Send to origin channel
        if sendto == 1:
            await ctx.send(embed=emb)
        # Send to user direct messages
        elif sendto == 2:
            await ctx.author.send(embed=emb)
        # Send to origin channel alternate
        elif sendto == 3:
            await ctx.channel.send(embed=emb)
        # Send to specified user
        elif sendto == 4 and not user is None:
            try:
                await user.send(embed=emb)
            except:
                # If no such user, send back command fail
                emb.description = "An error occurred."
                await ctx.author.send(embed=emb)

    # Command allmembers, prints all members across all server that the bot is present in.
    @bot.command(pass_context=True, aliases=["allmem", "am"], brief="In console, sends users from each server.",
                 description="In console, sends users and the guild they are from, across all servers the bot is "
                             "in.\n\n**Usage:**\n&allmembers")
    async def allmembers(self, ctx):
        for guild in self.bot.guilds:
            for member in guild.members:
                print(guild, member)
        await self.embed(ctx, "See console.")

    # Command members, a subset command of allmembers made into its' own that sends a list of all users in a server
    # to the command caller.
    @bot.command(pass_context=True, aliases=["mem"], brief="Send list of server users.",
                 description="Sends list of all members in the server this command is called.\n\n**Usage:**\n&members")
    async def members(self, ctx):
        the_guild = ctx.guild
        guild_members = ''
        count = 1
        for member in the_guild.members:
            guild_members = guild_members + str(
                count) + ': ' + member.name + '\n'
            count = count + 1
        await self.embed(ctx, 'List of guild members in {0}: \n'.format(the_guild) + guild_members, 2)

    # Command clearbot, clears all messages from the bot within dms.
    @bot.command(pass_context=True, aliases=["cbot", "clb"], brief="Delete bot Dms.",
                 description="Calling this command will delete all messages sent in Dms by the "
                             "bot.\n\n**Usage:**\n&clearbot")
    async def clearbot(self, ctx):
        dm = ctx.author.dm_channel
        bot_name = self.bot.user
        messageholder = []
        if dm != None:
            async for message in dm.history(limit=None):
                if message.author == bot_name:
                    messageholder.append(message)
                    # await message.delete()
            for msg in messageholder:
                await asyncio.sleep(0.9)
                await msg.delete()
            await self.embed(ctx, "DMs deleted.", 2)

    # Command clear, deletes all messages from a channel in one go.
    @bot.command(pass_context=True, aliases=["cl"], brief="Clear a text channel.",
                 description="Calling this command will delete all messages sent within the origin text "
                             "channel.\n\n**Usage:**\n&clear")
    async def clear(self, ctx):
        count = 0
        async for message in ctx.channel.history(limit=None):
            count += 1
        await ctx.channel.purge(limit=count)
        await self.embed(ctx, "All channel messages have been deleted.")

    # Command purge, deleting the number of messages dictated in field 'num'. 'All' used in command clear instead,
    # 'my' replaced with targetted deletion. Limit of purge is 50, with the bot only being able to purge messages
    # within the channel.
    @bot.command(pass_context=True, aliases=["prg"], brief="Delete some messages from a text channel.",
                 description="Given a number of messages and a user, delete that amount of messages from said person "
                             "from the text channel of origin. If 'all' is called as number, all messages from the "
                             "person will be deleted. If there is no user given, then the command will default to the "
                             "most recent messages. If no number is given, then the command will default to zero "
                             "messages to delete.\n\n**Usage:**\n&purge {number} {username}\n&purge {number} {"
                             "@username}\n&purge {number} {username#1234}\n&purge {number}\n&purge")
    async def purge(self, ctx, num='0', id=""):

        counter = 0

        try:
            num = int(num)
        except ValueError:
            if num == 'All' or num == 'all' or num == 'ALL':
                return await self.clear(ctx)
            else:
                return await self.embed(ctx, "Command Failed: That's not a valid input.")

        if num > 50:
            return await self.embed(ctx, 'Command Failed: Too many messages to delete, please keep it under 50.')
        elif num <= 0:
            return await self.embed(ctx, 'Command Failed: Choose a number greater than 0.')

        if id == "":
            await ctx.channel.purge(limit=num)
        else:
            async for message in ctx.channel.history(limit=None):
                print('author: {0}'.format(str(message.author)))
                print('wanted: {0}'.format(id))
                if str(
                        str(message.author)
                ) == id or message.author.name == id or message.author.mention == id:
                    counter += 1
                    await message.delete()
                    if counter == num:
                        break
        await self.embed(ctx, "Messages deleted.")


async def setup(bot):
    await bot.add_cog(Private(bot))
