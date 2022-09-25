#Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands

import random

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
        await ctx.message.delete()

    #Command purge, deleting the number of messages dictated in field 'num'. 'num' must also be convertible to type int or else the command will not work. Thinking of working on changing this fact, by adding keywords like 'all' or 'my' with a third redundant field that only works when the other keywords are in effect.
    @bot.command(pass_context=True)
    async def purge(self, ctx, num):
        num = int(num)
        if num > 50:
            await ctx.send(
                'Too many messages to delete, please keep it under 50.')
            return
        await ctx.channel.purge(limit=num)

    #Command talk, by calling command and an name into the 'user' field it searches the server to find if such a person exists, if they do it sends a randomized message to them. Although basic, it is a legacy command from the original project. Perhaps it could be expanded on.
    @bot.command(pass_context=True)
    async def talk(self, ctx, user):
        all_members = ctx.guild.members
        print('user: ' + user)
        for member in all_members:
            print('member name: ' + member.name)
            if member.name == user:
                if member.bot == True:
                    await ctx.send("This is a bot, cannot send message.")
                    return
                new_message = random.choice(messages)
                await member.send(ctx.author.name + ' to ' + member.name +
                                  ': ' + new_message)
                await ctx.author.send('You to ' + member.name + ': ' +
                                      new_message)
                return
        await ctx.send("This person does not exist.")
        return

    @bot.command(pass_context=True)
    async def join(self, ctx):
        #joins the discord vc
        channel = ctx.message.author.voice.channel
        await channel.connect()


def setup(bot):
    bot.add_cog(Public(bot))
