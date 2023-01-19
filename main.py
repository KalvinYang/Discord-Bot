# Roomz Bot - Your personal discord bot that helps you throughout your server!
# Roomz Bot originally was a connection bot, but the scope of the project has now been extended to a multi-purpose bot that can help with your server experience.
# It doesn't matter how big or small the server is. It works for all sizes!

# To do list:
# 1. Image Searching that sends designated amount of relevant photos.
# 2. Fastforwarding \  |2-3:Seek Command        |
# 3. Rewinding      /  |   (Nilson working on)  |
# 4. Remake help command (use briefs, aliases and descriptions)------------------------------Done
# 5. Search youtube and play song from chosen search
# 6. Finish descriptions, aliases and briefs for each functions------------------------------Done
# 7. Line by line documentation
# 8. More math functions (build off of each other)
# 9. Make simple games (make games cog)
# 10. Learn and implement database for the items below
# 11. Server leveling system
# 12. Saved games, simple and accessable
# 13. Inventories, save across games (coins and such)
# 14. Make larger scale, think shoob, karuta, epic rpg
# 15. Event planner
# 16. Local schedule database for server (upload/update own planner, i.e. "&schedule @stevethestevemon" will pull up a picture with that person's schedule. "&edit_schedule *link*" to edit your schedule.)
# 17. Make a secret santa cog setup cog (SS cog)
# 18. Make functions in SS to randomize people and produce a list of cooresponding secret santas
# 19. Make functions that auto deliver their secret santas just in case the original message sender doesn't want to know who gets who
# 20. Make open-ai cog (OA cog) that will connect to open-ai and be capable of sending inputs and sending back the results
# 21. Make multi function that calls multiple functions in one line

# Make sure you hit green run button before you try bot commands! otherwise bot is offline

# Base import needed to connect bot.
import os

# Discord imports allow for easy access to connection to discord and making commands.
import discord
from ZZBotToken import Token
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CommandInvokeError
from discord.ext.commands import BadArgument

# Random import currently used for randomly choosing a message to send to people. Later perhaps used to choose a song
# or in a game that can be attached to the project.
import random

# This import is currently used in stalling the deleting of messages from the bot.
import asyncio

# Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

# Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

# This variable has to do with the bot's private token, allowing connection
# to specific bot within anyone else connecting to the specific bot.
# my_secret = os.environ['token']

# Starts up extensions i.e. our commands
startup_extensions = ["private", "public", "music", "mathy"]

# Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")

# List of messages, currently from the first build, thinking of perhaps using a database for commands and messages,
# but will currently stick to this to allow code to continue to work for now.
messages = [
    'Hello there!', "Hey what's up?", 'How are you doing?', 'Nice to meet you!',
    "We're here to talk to you about your car's extended warranty.",
    "This is the government, here to say that your social security card is out of date.", "Want to hop in vc?"
]


# When the bot connects it will print that statement to allow dev to know of successful connection.
@bot.event
async def on_connect():
    print('{0.user} has been logged in.'.format(bot))


# When the bot is ready to be used it will print statement to allow dev to know of bot being ready.
@bot.event
async def on_ready():
    print('{0.user} is ready.'.format(bot))


# Still testing these
# ----------------------------------------------------
@bot.event
async def on_member_join(member):
    member.send(
        'Welcome to {0}, glad to have you and have a nice stay!'.format(
            member.guild))


@bot.event
async def on_invite_create(ctx):
    ctx.guild.owner.send(
        'Someone has created an invite for channel: {0}'.format(ctx.channel))


# ----------------------------------------------------

# This is whenever there are command errors, these will be checked and outputted as needed.
# @bot.event
# async def on_command_error(ctx, error):
#    if isinstance(error, CommandNotFound):
#        await ctx.channel.send('Error: CommandNotFound')
#        return
#    elif isinstance(error, CommandInvokeError):
#        await ctx.channel.send('Error: CommandInvokeError')
#        return
#    elif isinstance(error, BadArgument):
#        await ctx.channel.send('Error: BadArgument')
#        return


# Command help, sending the list of current commands to the author of the command. Takes the briefs, descriptions
# and/or aliases from each command and compiles them based on 'searchcommand', then sends back the result.
@bot.command(pass_context=True, brief="List of all commands")
async def help(ctx, searchcommand=""): \
        # Setting up basic embed with color chosen
    emb = discord.Embed(color=0x3498db)
    # Puts up your name, and your profile picture to show that you called the function |
    # url=discord.embeds.EmptyEmbed is filled as Null
    emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    # Puts the thumbnail of the embed as the bot profile picture
    emb.set_thumbnail(url=bot.user.avatar)
    # Base case of empty 'searchcommand', sends all commands connected to current bot with briefs only.
    if searchcommand == "":
        # Set embed title
        emb.title = "Commands"
        count = 0
        # Going through each cog
        for cog in startup_extensions:
            # Blank character for adding fields
            the_value = "\u200b"
            # Get help command in the embed
            if count == 0:
                help_command = bot.get_command("help")
                help_command = "**&" + help_command.name + ":** " + help_command.brief
                the_value = help_command
                count = 1
            # Spacing between cogs
            emb.add_field(name=the_value, value="\u200b", inline=False)
            # Get cog object, and cog commands
            cog_name = cog.capitalize()
            cog_object = bot.get_cog(cog_name)
            cog_commands = cog_object.get_commands()
            # Spacer
            command_send = "--------------------------------------------------\n"
            # Add commands and their briefs
            for cmnd in cog_commands:
                command_send += '**&' + cmnd.name + ':** ' + cmnd.brief + '\n'
            # Adds field with cog as field name, and 'command_send' as value
            emb.add_field(name="**" + cog_name + "**", value=command_send, inline=False)
        # Ping user and send message
        await ctx.send('{0} Check Your DMs'.format(ctx.author.mention))
        await ctx.author.send(embed=emb)
        # Delete ping if possible
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            return
    # If 'searchcommand' is a cog
    elif searchcommand in startup_extensions:
        # Find which cog it is
        for cog in startup_extensions:
            if cog == searchcommand or cog.capitalize() == searchcommand:
                # Set embed title
                cog_name = cog.capitalize()
                emb.title = cog_name + " Commands"
                # Get commands
                cog_object = bot.get_cog(cog_name)
                cog_commands = cog_object.get_commands()
                # Spacer
                command_send = "--------------------------------------------------\n"
                # Setup commands and their briefs as embed description
                for cmnd in cog_commands:
                    command_send += "**&" + cmnd.name + ':** ' + cmnd.brief + '\n\n'
                emb.description = command_send
                # Ping and send message, then delete ping if possible
                await ctx.send('{0} Check Your DMs'.format(ctx.author.mention))
                await ctx.author.send(embed=emb)
                try:
                    await ctx.message.delete()
                except discord.Forbidden:
                    return
    else:
        # See if 'searchcommand' is a command or a command alias
        for c in bot.commands:
            if searchcommand == c.name or searchcommand in c.aliases:
                # Set embed title and description
                emb.title = "&" + c.name
                command_send = c.description + "\n\n**Aliases:**\n"
                # Checking for aliasses
                if c.aliases == []:
                    command_send += "None"
                else:
                    for alias in c.aliases:
                        command_send += alias + ', '
                emb.description = command_send
                # Ping user and send message, then delete ping if possible
                await ctx.send('{0} Check Your DMs'.format(ctx.author.mention))
                await ctx.author.send(embed=emb)
                try:
                    await ctx.message.delete()
                    return
                except discord.Forbidden:
                    return
        # Nothing matched 'searchcommand' send
        emb.title = "Nothing came up"
        emb.description = "Sorry there is no such command or section."
        await ctx.author.send(embed=emb)


# Event on_message, currently only has basic functionality to delete it's own messages to reduce clutter. line 'await
# bot.process_commands(message_1)' allows for commands to work despite the inclusion of this event. Otherwise the
# other commands would be ignored due to a coroutine.
@bot.event
async def on_message(message_1):
    # Line below used to allow commands to run in tandem with deleting the message.
    await bot.process_commands(message_1)

    # Checks if the message is from the bot
    if message_1.author == bot.user:
        # Makes sure it is a specific message
        if message_1.content.endswith('Check Your DMs'):
            # Wait and then delete message
            await asyncio.sleep(3)
            await message_1.delete()
    return


# On startup load all extensions in 'startup_extensions' list of extensions
if __name__ == "__main__":
    for extension in startup_extensions:
        asyncio.run(bot.load_extension(extension))

# Running bot
bot.run(Token)

# --------------------------------------------------------------------------------------------------

# Below is legacy code, remanants from the original project used to build portions of the new code. Left in just in
# case there is inspiration to still be taken from it.

# https://assemblyai.notion.site/assemblyai/AssemblyAI-Hackathon-Quickstart-76cf5c07aeff4f06ba9ac193899c0a4b

# count = 0
# code_names = {}
# names = message_1.guild.members
# keys_of_codenames = []
# if fst_login == 0:
# for x in names:
#   count = count + 1
#  code_names[count] = x
# keys_of_codenames = list(code_names.keys())
# print(keys_of_codenames)
# fst_login = 1

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
# await message_1.channel.purge(limit=1)
# name_find = code_names[names.index(message_1.author)]
#      await user.send('Anon' + ': ' + message)
#      await message_1.author.send('You: ' + message)
