#Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands
import random
import asyncio

#Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

#Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

#List of messages, currently from the first build, thinking of perhaps using a database for commands and messages, but will currently stick to this to allow code to continue to work for now.
messages = [
    'Hello there!', "Hey what's up?", 'How are you doing?', 'Nice to meet you!'
]

#List of commands, currently out of date, however, by making the command list like this, it allows for an easy read of all the commands that are currently implemented into the bot.
command_desc = {
    "&help": " = &h, lists all commands.",
    "&talk": " = &t, connect to a random person and talk.",
    "&letters": " = &l, checks all new letters in mail.",
    "&save":
    " = &s, save any current letter being viewed if not already saved.",
    "&inventory": " = &i, view all saved letters.",
    "&join": " = &j, joins voice channel."
}
the_commands = list(command_desc.keys())

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")


class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Command help, sending the list of current commands to the author of the command. It builds the paragraph manually from the parts in the command list and then mentions the author to check DMs. After of which it deletes the original command.
    @bot.command(pass_context=True)
    async def help(self, ctx):
        command_send = "Commands Include:\n"
        for i in the_commands:
            command_send = command_send + i + command_desc[i] + '\n'
        await ctx.send('{0} Check Your DMs'.format(ctx.author.mention))
        await ctx.author.send(command_send)
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            return

    #Command talk, by calling command and an name into the 'user' field it searches the server to find if such a person exists, if they do it sends a randomized message to them. Although basic, it is a legacy command from the original project. Perhaps it could be expanded on.
    #Edit: Now only sends randomized messages when 'msg' field is empty. Otherwise will send intended message to 'user' so long as they are within the server.
    @bot.command(pass_context=True)
    async def talk(self, ctx, user, msg=""):
        all_members = ctx.guild.members
        print('user: ' + user)
        if user == ctx.author.name or user == ctx.author or user == ctx.author.mention:
            await ctx.send("Why are you sending a message to yourself?")
            return
        for member in all_members:
            print('member name: ' + member.name)
            if member.name == user or member == user or member.mention == user:
                if member.bot == True:
                    await ctx.send("This is a bot, cannot send message.")
                    return
                if msg == "":
                    new_message = random.choice(messages)
                else:
                    new_message = msg
                await member.send(ctx.author.name + ' to ' + member.name +
                                  ': ' + new_message)
                await ctx.author.send('You to ' + member.name + ': ' +
                                      new_message)
                return
        await ctx.send("This person does not exist in this server.")
        return
    #Command randomnum, chooses a random number from 0 to 10 by default. Chooses random number between 0 and indicated otherwise.
    @bot.command(pass_context=True)
    async def randomnum(self, ctx, num=10):
        somenumber = random.randrange(num)
        await ctx.send('Number: {0}'.format(somenumber))

    #Command saynum, sends separate messages counting from 1 to indicated number, so long as it is within 50 to minimize clutter.
    @bot.command(pass_context=True)
    async def saynum(self, ctx, num=0):
        if num <= 0:
            await ctx.channel.send('Cannot count to that number.')
            return
        elif num > 50:
            await ctx.channel.send('Max count limit is 50.')
            return
        for number in range(num):
            await asyncio.sleep(0.75)
            await ctx.channel.send('{0}'.format(number + 1))


def setup(bot):
    bot.add_cog(Public(bot))
