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
        self.ecolor = 0x3498db

    #Embedding for message ui looking better, automatically set to sending to origin channel
    async def embed(self, ctx, message="", sendto=1, user=None):
        #Take cog color (self.ecolor) as color, and command name as title
        emb = discord.Embed(color=self.ecolor,
                            title=str(ctx.command).capitalize() + " Results:")
        #Sets the user that called command as author by taking their name and pfp
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
        elif sendto == 4 and not user == None:
            try:
                await user.send(embed=emb)
            except:
                # If no such user, send back command fail
                emb.description = "An error occurred."
                await ctx.author.send(embed=emb)

    # Command talk, by calling command and an name into the 'user' field it searches the server to find if such a
    # person exists, if they do it sends a randomized message to them. Although basic, it is a legacy command from
    # the original project. Perhaps it could be expanded on. Edit: Now only sends randomized messages when 'msg'
    # field is empty. Otherwise will send intended message to 'user' so long as they are within the server.
    @bot.command(
        pass_context=True,
        aliases=['t', 'T', "ta", "Ta"],
        brief="DM server member through bot",
        description=
        "Send a custom message to another member of the same server through the bot. You will receive an identical "
        "message with 'You:' identifying yourself. If a message comes through the sender's username will be in the "
        "same format. If no message is included randomly choose one from bot.\n\n**Usage:**\n&talk {username} {"
        "message}\n&talk {@username} {message}\n&talk {username#1234} {message}\n&talk {username}\n&talk {"
        "@username}\n&talk {username#1234} "
    )
    async def talk(self, ctx, user, msg=""):
        all_members = ctx.guild.members
        print('user: ' + user)
        if user == ctx.author.name or user == str(ctx.author) or user == ctx.author.mention:
            await self.embed(ctx, "Why are you sending a message to yourself? Anyways, here's your message.\n\n" + msg,
                             2)
            return
        for member in all_members:
            print('member name: ' + member.name)
            if member.name == user or str(member) == user or member.mention == user:
                if member.bot:
                    await self.embed(ctx, "This is a bot, cannot send message them.")
                    return
                if msg == "":
                    new_message = random.choice(messages)
                else:
                    new_message = msg
                await self.embed(ctx, ctx.author.name + ' to ' + member.name +
                                 ':\n\n' + new_message, 4, member)
                await self.embed(ctx, 'You to ' + member.name + ':\n\n' +
                                 new_message, 2)
                return
        await self.embed(ctx, "This person does not exist in this server.")
        return

    #

    @bot.command(
        pass_context=True,
        aliases=['srn', 'srand', 'SRN'],
        brief="Spam channel with a random number of times",
        description=
        "Given a number, or default setting of 10, randomly choose from 0 to given number. Then send that number of "
        "messages to the channel the initial message came from.\n\n**Usage:**\n&sayrandnum {number}\n&sayrandnum "
    )
    async def sayrandnum(self, ctx, num=10):
        await self.embed(ctx, "Count to:")
        num = await self.randomnumber(ctx, num)
        await self.saynumber(ctx, num)

    #Command randomnum, chooses a random number from 0 to 10 by default. Chooses random number between 0 and indicated otherwise.
    @bot.command(
        pass_context=True,
        aliases=["randnum", "rn", "randomnum"],
        brief="Get a random number",
        description=
        "Given a number, or default setting of 10, randomly choose from 0 to given number, then send that number to the original channel.\n\n**Usage:**\n&randomnumber {number}\n&randomnumber"
    )
    async def randomnumber(self, ctx, num=10):
        somenumber = random.randrange(num)
        await self.embed(ctx,'Number: {0}'.format(somenumber))
        return somenumber

    #Command saynum, sends separate messages counting from 1 to indicated number, so long as it is within 50 to minimize clutter.
    @bot.command(
        pass_context=True,
        aliases=["sn", "sayn", "saynum"],
        brief="Counts to given number",
        description=
        "Given a number, send messages from 1 to given number to the original channel, if no number is given, default to 0. Minimum amount being 0 and maximum being 50.\n\n**Usage:**\n&saynumber {number}\n&saynumber"
    )
    async def saynumber(self, ctx, num=0):
        if num <= 0:
            await self.embed(ctx, 'Cannot count to that number.', 3)
            return
        elif num > 50:
            await self.embed(ctx, 'Max count limit is 50.', 3)
            return
        for number in range(num):
            await asyncio.sleep(0.75)
            await self.embed(ctx, '{0}'.format(number + 1), 3)

    # Command guessnum, guess a number between 0 and 10, randomizes number and tells you if you got it right. Auto
    # allows for auto guessing until the number is achieved and returns the amount of guesses needed.
    @bot.command(
        pass_context=True,
        aliases=["gn", "guessnum", "gnum"],
        brief="Guess the bot's hidden number",
        description=
        "Guess a number between 0 and 10, if it matches the bot's hidden number you win, the hidden number randomizes "
        "each time the command is called. Auto guessing by inputting 'yes', messaging back the number of randomizes "
        "it took your guess to match the bot's hidden number.\n\n**Usage:**\n&guessnumber {number}\n&guessnumber {"
        "number} {yes} "
    )
    async def guessnumber(self, ctx, num=-1, auto='no'):
        if num < 0 or num > 10:
            await self.embed(ctx, 'Not a valid guess.', 3)
            return
        if auto == 'yes' or auto == 'y' or auto == 'Y' or auto == 'YES' or auto == 'Yes':
            counter = 0
            while True:
                somenumber = random.randrange(11)
                counter += 1
                if somenumber == num:
                    await self.embed(ctx,
                                     'You took {0} guess(es) to get it right.'.format(
                                         counter))
                    return
        somenumber = random.randrange(11)
        print('guess: {0}'.format(num))
        print('value: {0}'.format(somenumber))
        if somenumber == num:
            await self.embed(ctx, 'You guessed right!', 3)
        else:
            await self.embed(ctx, 'WRONG.', 3)


async def setup(bot):
    await bot.add_cog(Public(bot))
