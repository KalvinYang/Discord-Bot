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

#Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

#Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

#This variable has to do with the bot's private token, allowing connection to specific bot within anyone else connecting to the specific bot.
my_secret = os.environ['token']

#Starts up extensions i.e. our commands
startup_extensions = ["private", "public"]

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")

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


if __name__ == "__main__":
    for extension in startup_extensions:
        bot.load_extension(extension)
bot.run(os.getenv('token'))

#Runs the bot

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
