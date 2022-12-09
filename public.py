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

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")

#List of messages, currently from the first build, thinking of perhaps using a database for commands and messages, but will currently stick to this to allow code to continue to work for now.
messages = [
    'Hello there!', "Hey what's up?", 'How are you doing?', 'Nice to meet you!'
]

class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    #Command talk, by calling command and an name into the 'user' field it searches the server to find if such a person exists, if they do it sends a randomized message to them. Although basic, it is a legacy command from the original project. Perhaps it could be expanded on.
    #Edit: Now only sends randomized messages when 'msg' field is empty. Otherwise will send intended message to 'user' so long as they are within the server.
    @bot.command(pass_context=True,aliases=['t', 'T',"ta","Ta"],brief="DM server member through bot", description="Send a custom message to another member of the same server through the bot. You will recieve an identical message with 'You:' identifying yourself. If a message comes through the sender's username will be in the same formet. If no message is included randomly choose one from bot.\n\nUsage:\n&talk {username} {message}\n&talk {@username} {message}\n&talk {username#1234} {message}\n&talk {username}\n&talk {@username}\n&talk {username#1234}")
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
#
    @bot.command(pass_context=True,aliases=['srn', 'srand', 'SRN'],brief="Spam channel with a random number of times",description="Given a number, or default setting of 10, randomly choose from 0 to given number. Then send that number of messages to the channel the initial message came from.\n\nUsage:\n&sayrandnum {number}\n&sayrandnum")
    async def sayrandnum(self,ctx, num=10):
        await ctx.send("Count to:")
        num = await self.randomnumber(ctx,num)
        await self.saynumber(ctx, num)
      
    #Command randomnum, chooses a random number from 0 to 10 by default. Chooses random number between 0 and indicated otherwise.
    @bot.command(pass_context=True,aliases=["randnum","rn","randomnum"],brief="Get a random number",description="Given a number, or default setting of 10, randomly choose from 0 to given number, then send that number to the original channel.\n\nUsage:\n&randomnumber {number}\n&randomnumber")
    async def randomnumber(self, ctx, num=10):
        somenumber = random.randrange(num)
        await ctx.send('Number: {0}'.format(somenumber))
        return somenumber

    #Command saynum, sends separate messages counting from 1 to indicated number, so long as it is within 50 to minimize clutter.
    @bot.command(pass_context=True,aliases=["sn","sayn","saynum"],brief="Counts to given number",description="Given a number, send messages from 1 to given number to the original channel, if no number is given, default to 0. Minimum amount being 0 and maximum being 50.\n\nUsage:\n&saynumber {number}\n&saynumber")
    async def saynumber(self, ctx, num=0):
        if num <= 0:
            await ctx.channel.send('Cannot count to that number.')
            return
        elif num > 50:
            await ctx.channel.send('Max count limit is 50.')
            return
        for number in range(num):
            await asyncio.sleep(0.75)
            await ctx.channel.send('{0}'.format(number + 1))

    #Command guessnum, guess a number between 0 and 10, randomizes number and tells you if you got it right. Auto allows for auto guessing until the number is achieved and returns the amount of guesses needed.
    @bot.command(pass_context=True,aliases=["gn","guessnum","gnum"],brief="Guess the bot's hidden number",description="Guess a number between 0 and 10, if it matches the bot's hidden number you win, the hidden number randomizes each time the command is called. Auto guessing by inputting 'yes', messaging back the number of randomizes it took your guess to match the bot's hidden number.\n\nUsage:\n&guessnumber {number}\n&guessnumber {number} {yes}")
    async def guessnumber(self, ctx, num=-1, auto='no'):
        if num < 0 or num > 10:
            await ctx.channel.send('Not a valid guess.')
            return
        if auto == 'yes' or auto == 'y' or auto == 'Y' or auto == 'YES' or auto == 'Yes':
            counter = 0
            while True:
                somenumber = random.randrange(11)
                counter += 1
                if somenumber == num:
                    await ctx.send(
                        'You took {0} guess(es) to get it right.'.format(
                            counter))
                    return
        somenumber = random.randrange(11)
        print('guess: {0}'.format(num))
        print('value: {0}'.format(somenumber))
        if somenumber == num:
            await ctx.channel.send('You guessed right!')
        else:
            await ctx.channel.send('WRONG.')


def setup(bot):
    bot.add_cog(Public(bot))
