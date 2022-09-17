#Roomz Bot - Your personal discord bot that helps you throughout your server!
#Roomz Bot originally was a connection bot, but the scope of the project has now been extended to a multi-purpose bot that can help with your server experience.
#It doesn't matter how big or small the server is. It works for all sizes!

#Make sure you hit green run button before you try bot commands! otherwise bot is offline

#Base import needed to connect bot.
import os

#Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands

#Random import currently used for randomly choosing a message to send to people. Later perhaps used to choose a song or in a game that can be attached to the project.
import random

#This import is currently used in stalling the deleting of messages from the bot.
import asyncio

#Itents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

#Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")

#List of commands, currently out of date, however, by making the command list like this, it allows for an easy read of all the commands that are currently implemented into the bot.
command_desc = {
    "&help": " = &h, lists all commands.",
    "&talk": " = &t, connect to a random person and talk.",
    "&letters": " = &l, checks all new letters in mail.",
    "&save":
    " = &s, save any current letter being viewed if not already saved.",
    "&inventory": " = &i, view all saved letters."
}
the_commands = list(command_desc.keys())

#This variable has to do with the bot's private token, allowing connection to specific bot within anyone else connecting to the specific bot.
my_secret = os.environ['token']

#List of messages, currently from the first build, thinking of perhaps using a database for commands and messages, but will currently stick to this to allow code to continue to work for now.
messages = [
    'Hello there!', "Hey what's up?", 'How are you doing?', 'Nice to meet you!'
]


#When the bot connects it will print that statement to allow dev to know of successful connection.
@bot.event
async def on_connect():
    print('{0.user} has been logged in.'.format(bot))


#When the bot is ready to be used it will print statement to allow dev to know of bot being ready.
@bot.event
async def on_ready():
    print('{0.user} is ready.'.format(bot))


#Command help, sending the list of current commands to the author of the command. It builds the paragraph manually from the parts in the command list and then mentions the author to check DMs. After of which it deletes the original command.
@bot.command(pass_context=True)
async def help(ctx):
    command_send = "Commands Include:\n"
    for i in the_commands:
        command_send = command_send + i + command_desc[i] + '\n'
    await ctx.send('{0} Check Your DMs'.format(ctx.author.mention))
    await ctx.author.send(command_send)
    await ctx.message.delete()


#Command purge, deleting the number of messages dictated in field 'num'. 'num' must also be convertible to type int or else the command will not work. Thinking of working on changing this fact, by adding keywords like 'all' or 'my' with a third redundant field that only works when the other keywords are in effect.
@bot.command(pass_context=True)
async def purge(ctx, num):
    num = int(num)
    await ctx.channel.purge(limit=num)


#Command allmembers, originally called 'members' a piece of code taken and used to debug as to why the bot could only view itself when searching in guilds. It lists all users in every server that the bot is within, however list is only available within console.
@bot.command(pass_context=True)
async def allmembers(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            print(guild, member)


#Command members, a subset command of allmembers made into its' own that sends a list of all users in a server to the command caller.
@bot.command(pass_context=True)
async def members(ctx):
    the_guild = ctx.guild
    guild_members = ''
    count = 1
    for member in the_guild.members:
        count = count + 1
        guild_members = guild_members + str(count) + ': ' + member.name + '\n'
    await ctx.author.send(
        'List of guild members in {0}: \n'.format(the_guild) + guild_members)


#Command talk, by calling command and an name into the 'user' field it searches the server to find if such a person exists, if they do it sends a randomized message to them. Although basic, it is a legacy command from the original project. Perhaps it could be expanded on.
@bot.command(pass_context=True)
async def talk(ctx, user):
    all_members = ctx.guild.members
    print('user: ' + user)
    for member in all_members:
        print('member name: ' + member.name)
        if member.name == user:
            if member.bot == True:
                await ctx.send("This is a bot, cannot send message.")
                return
            new_message = random.choice(messages)
            await member.send(ctx.author.name + ' to ' + member.name + ': ' +
                              new_message)
            await ctx.author.send('You to ' + member.name + ': ' + new_message)
            return
    await ctx.send("This person does not exist.")
    return


#Event on_message, currently only has basic functionality to delete it's own messages to reduce clutter. line 'await bot.process_commands(message_1)' allows for commands to work despite the inclusion of this event. Otherwise the other commands would be ignored due to a coroutine.
@bot.event
async def on_message(message_1):
    await bot.process_commands(message_1)
    if message_1.author == bot.user:
        if message_1.content.endswith('Check Your DMs'):
            await asyncio.sleep(3)
            await message_1.delete()
        elif message_1.content.startswith('Commands Include:'):
            await asyncio.sleep(10)
            await message_1.delete()
    return


#Runs the bot
bot.run(os.getenv('token'))







#Below is legacy code, remanants from the original project used to build portions of the new code. Left in just in case there is inspiration to still be taken from it.

#https://assemblyai.notion.site/assemblyai/AssemblyAI-Hackathon-Quickstart-76cf5c07aeff4f06ba9ac193899c0a4b

#count = 0
#code_names = {}
#names = message_1.guild.members
#keys_of_codenames = []
#if fst_login == 0:
#for x in names:
#   count = count + 1
#  code_names[count] = x
#keys_of_codenames = list(code_names.keys())
#print(keys_of_codenames)
#fst_login = 1

#  elif message_1.content.startswith('&talk') or message_1.content.startswith(
#          '&t'):
#      users = message_1.guild.members
#      user = random.choice(users)
#      print(message_1.author, user)  #checks to whom the msg is sent to.
#     if message_1.author == user:
#          message = 'This is yourself!'
#      elif str(user) == 'Roomz Bot#9241':
#          await message_1.delete()
#          #await message_1.channel.purge(limit=1)
#          return None
#      else:
#          message = random.choice(messages)
#      await message_1.delete()
#await message_1.channel.purge(limit=1)
#name_find = code_names[names.index(message_1.author)]
#      await user.send('Anon' + ': ' + message)
#      await message_1.author.send('You: ' + message)
