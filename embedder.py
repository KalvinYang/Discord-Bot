import discord
from discord.ext import commands

# Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

# Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')


class Embedder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Embedding for message ui looking better, automatically set to sending to origin channel
    async def embed(ctx, message="", sendto=1, user=None, bot_level="", fieldmsg="", fieldt1="", fieldt2="", ecolor=""):
        # Take cog color (self.ecolor) as color, and command name as title
        if bot_level == "":
            if ecolor == "":
                emb = discord.Embed(color=ctx.cog.ecolor,
                                    title=str(ctx.command).capitalize() + " Results:")
            else:
                emb = discord.Embed(color=ecolor,
                                    title=str(ctx.command).capitalize() + " Results:")
        else:
            if ecolor == "":
                emb = discord.Embed(color=ctx.cog.ecolor,
                                    title=bot_level)
            else:
                emb = discord.Embed(color=ecolor,
                                    title=bot_level)
        # Sets the user that called command as author by taking their name and pfp
        emb.set_author(name=ctx.author.display_name,
                       icon_url=ctx.author.avatar)
        # Set message of embed (add secondary field if fieldmsg is set to something else) TO DO: Add more then 1 field
        if fieldmsg != "":
            emb.add_field(name=fieldt1, value=message, inline=True)
            emb.add_field(name=fieldt2, value=fieldmsg, inline=True)
        else:
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


async def setup(bot):
    await bot.add_cog(Embedder(bot))
