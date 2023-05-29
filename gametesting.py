# Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands
import sqlite3

# Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

# Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

# Setting up database
db = sqlite3.connect('testing_db')
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS main(guild_id TEXT, msg TEXT, channel_id TEXT, author TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, level INT, xp INT)''')


class Gametesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ecolor = 0xad1457

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

    # Checks for valid numerical indexes
    async def isint(self, ctx, index):
        try:
            index = int(index)
            if index < 1:
                await self.embed(ctx, "Command Failed: Please insert an index greater then 0.", sendto=2)
                return False
            return True
        except TypeError or ValueError:
            await self.embed(ctx, "Command Failed: Index invalid.")
            return False

    # Checks for valid indexes for messages in database
    async def msgcheck(self, ctx, index):
        c.execute("SELECT msg FROM main WHERE author=?", (str(ctx.author),))
        all_messages = c.fetchall()
        try:
            index = int(index)
        except ValueError:
            await self.embed(ctx, "Command Failed: Invalid index.", sendto=2)
            return 0
        if all_messages is None:
            await self.embed(ctx, "Command Failed: No messages found.", sendto=2)
            return 0
        elif len(all_messages) < (index - 1):
            await self.embed(ctx, "Command Failed: index outside of amount of saved messages.", sendto=2)
            return 0
        try:
            msg = all_messages[index - 1]
            msg = str(msg[0])
            return msg
        except IndexError:
            await self.embed(ctx, "Command Failed: Index outside of range.", sendto=2)
            return 0

    # When bot is ready add everyone to database at level 0
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                c.execute("SELECT username FROM users WHERE username=?", (str(member.name),))
                user = c.fetchone()
                if user is None:
                    db.execute("INSERT INTO users (username,level,xp) VALUES(?,?,?)",
                               (str(member.name), 0, 0))
                    db.commit()

    # When someone messages a channel, add xp to them, or level them up in bot database
    @commands.Cog.listener()
    async def on_message(self, message_1):
        usern = str(message_1.author.name)
        c.execute("SELECT level, xp FROM users WHERE username=?", (usern,))
        user = c.fetchone()
        if user is None:
            db.execute("INSERT INTO users (username,level,xp) VALUES(?,?,?)", (usern, 1, 0))
            db.commit()
        elif user[0] == 0:
            db.execute("UPDATE users SET level=1 WHERE username=?", (usern,))
            db.commit()
            await self.embed(message_1, "Level: 1\nXp: 0", sendto=3, bot_level="You Leveled Up!")
        else:
            xp = user[1]
            xp += 1
            level = user[0]
            if xp == (level * 10):
                level += 1
                db.execute("UPDATE users SET xp=0 , level=? WHERE username=?",
                           (level, usern,))
                db.commit()
                await self.embed(message_1, "Level: {0}\nXp: 0".format(str(level)), sendto=3,
                                 bot_level="You Leveled Up!")
            else:
                db.execute("UPDATE users SET xp=? WHERE username=?", (xp, usern,))
                db.commit()

    # Gathers level info on a user and sends it to them
    @bot.command(pass_context=True,
                 aliases=["lvl", "lv"],
                 brief="Find out your current level.",
                 description=
                 "Find out your level within the bot, level up by sending messages in servers that this bot is in."
                 "\n\n**Usage:**\n&level")
    async def level(self, ctx):
        usern = str(ctx.author)
        c.execute("SELECT level, xp FROM users WHERE username=?", (usern,))
        level_xp = c.fetchone()
        await self.embed(ctx, "Level: {0}\nXp: {1}".format(str(level_xp[0]), str(level_xp[1])),
                         bot_level="Your Current "
                                   "Level:")

    # Takes a string and saves it into database along with the guild, channel and user it came from.
    @bot.command(pass_context=True,
                 aliases=["smsg", "savemsg"],
                 brief="Save msg in bot.",
                 description=
                 "Save a message within the bot, saving the guild, channel, and user as well."
                 "\n\n**Usage:**\n&savemessage {'text'}")
    async def savemessage(self, ctx, msg=""):
        if ctx.guild is None:
            guild = "Dms"
        else:
            guild = str(ctx.guild)
        db.execute("INSERT INTO main (guild_id,msg,channel_id,author) VALUES(?,?,?,?)",
                   (guild, msg, str(ctx.channel), str(ctx.author)))
        db.commit()
        return await self.embed(ctx, "Your message has been saved.", 2)

    # Finds the indicated saved message in the database and deletes it from memory
    @bot.command(pass_context=True,
                 aliases=["dmsg", "delmsg"],
                 brief="Delete msg in bot.",
                 description=
                 "Save a message within the bot, saving the guild, channel, and user as well."
                 "\n\n**Usage:**\n&deletemessage {number}")
    async def deletemessage(self, ctx, index=-1):
        if not await self.isint(ctx, index):
            return
        msg = await self.msgcheck(ctx, index)
        if msg == 0:
            return
        db.execute("DELETE FROM main WHERE msg=?", (msg,))
        db.commit()
        return await self.embed(ctx, "Message Deleted.", 2)

    # Gathers all saved messages from the origin user and send back list of messages
    @bot.command(pass_context=True,
                 aliases=["mmsg", "mymsg"],
                 brief="Calls all saved msgs.",
                 description=
                 "Calls and returns all saved msgs in database."
                 "\n\n**Usage:**\n&mymessage")
    async def mymessage(self, ctx):
        res = "Your Messages:\n"
        count = 0
        for row in c.execute("SELECT guild_id, msg FROM main WHERE author=?", (str(ctx.author),)):
            count += 1
            res += str(count) + ". From: " + str(row[0]) + " | Message: " + str(row[1]) + '\n'
        return await self.embed(ctx, res, 2, )

    # From the list of messages in "mymessage" command, send the indicated message to the indicated user as long as they
    # are in the guild that the origin user called it in
    @bot.command(pass_context=True,
                 aliases=["ssmsg", "sendsmsg"],
                 brief="Sends a saved message to a person.",
                 description=
                 "Send a designed saved message by the index it is saved in the bot."
                 "\n\n**Usage:**\n&sendsavedmessage {number} {username}\n&sendsavedmessage {number} {"
                 "username#1234}\n&sendsavedmessage {number} {@username}")
    async def sendsavedmessage(self, ctx, index=-1, user=""):
        if not await self.isint(ctx, index):
            return
        elif user == "":
            return await self.embed(ctx, "Command Failed: Please indicate a user you want to send this message to.",
                                    sendto=2)
        msg = await self.msgcheck(ctx, index)
        if msg == 0:
            return
        try:
            all_members = ctx.guild.members
        except:
            return await self.embed(ctx, "Command Failed: Cannot call command outside of guilds.")
        if user == ctx.author.name or user == str(ctx.author) or user == ctx.author.mention:
            return await self.embed(ctx,
                                    "Why are you sending a message to yourself? Anyways, here's your message.\n\n" + msg,
                                    2)
        for member in all_members:
            if member.name == user or str(member) == user or member.mention == user:
                if member.bot:
                    return await self.embed(ctx, "This is a bot, cannot send message them.", sendto=2)
                await self.embed(ctx, ctx.author.name + ' to ' + member.name +
                                 ':\n\n' + msg, 4, member)
                return await self.embed(ctx, 'You to ' + member.name + ':\n\n' + msg, 2)
        await self.embed(ctx, "This person does not exist in this server.")


async def setup(bot):
    await bot.add_cog(Gametesting(bot))
