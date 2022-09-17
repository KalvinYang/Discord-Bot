import os
#Roomz Bot - Your personal discord bot that helps connect people together! Ver 0.0.0.2
#Roomz Bot is a bot that acts like Omegle. It helps to connect people together by randomly selecting anyone in the discord server and instantly starts a conversation for the user with that person!
#It doesn't matter how big or small the server is. It works for all sizes!

# so make sure you hit green run button before you try bot commands! otherwise bot is offline
import discord
from discord.ext import commands
import random
import asyncio

Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True
bot = commands.Bot(intents=Intents, command_prefix='&')
bot.remove_command("help")

command_desc = {
    "&help": " = &h, lists all commands.",
    "&talk": " = &t, connect to a random person and talk.",
    "&letters": " = &l, checks all new letters in mail.",
    "&save":
    " = &s, save any current letter being viewed if not already saved.",
    "&inventory": " = &i, view all saved letters."
}

the_commands = list(command_desc.keys())
my_secret = os.environ['token']
#my_secret = os.environ['token']

messages = [
    'Hello there!', "Hey what's up?", 'How are you doing?', 'Nice to meet you!'
]


@bot.event
async def on_connect():
    print('{0.user} has been logged in.'.format(bot))


@bot.event
async def on_ready():
    print('{0.user} is ready.'.format(bot))
    global fst_login
    fst_login = 0


@bot.command(pass_context=True)
async def help(ctx):
    command_send = "Commands Include:\n"
    for i in the_commands:
        command_send = command_send + i + command_desc[i] + '\n'
    await ctx.send('{0} Check Your DMs'.format(ctx.author.mention))
    await ctx.author.send(command_send)
    await ctx.message.delete()
    return


@bot.command(pass_context=True)
async def purge(ctx, num):
    num = int(num)
    await ctx.channel.purge(limit=num)


@bot.command(pass_context=True)
async def members(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            print(member)


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

bot.run(os.getenv('token'))
