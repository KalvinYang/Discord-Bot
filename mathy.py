#Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands

import re

#Intents allow for the usage of information within their classes.
Intents = discord.Intents.default().all()
Intents.members = True
Intents.presences = True
Intents.guilds = True

#Bot prefix setup and set the bot intentions to those setup above.
bot = commands.Bot(intents=Intents, command_prefix='&')

#Command allmembers, originally called 'members' a piece of code taken and used to debug as to why the bot could only view itself when searching in guilds. It lists all users in every server that the bot is within, however list is only available within console.

#Removal of help command, this is so that a custom help command can be built.
bot.remove_command("help")


class Mathy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Command add, simply finds the sum of all argument numbers together. Rounds to nearest int.
    @bot.command(pass_context=True)
    async def add(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("You didn't input anything to add.")
            return
        num = 0.0
        for number in args:
            try:
                num += float(number)
                print(num)
            except ValueError:
                await ctx.send(
                    'There is something that is not a number in here.')
                return
        num = int(round(num))
        await ctx.send('Sum: {0}'.format(num))

    #Command subtract, simply finds the difference of all argument numbers together, given the first number as the initial value. Rounds to nearest int.
    @bot.command(pass_context=True)
    async def subtract(self, ctx, num=0.0, *args):
        if len(args) == 1:
            await ctx.send("You didn't input anything to subtract.")
            return
        for number in args:
            try:
                num -= float(number)
            except ValueError:
                await ctx.send(
                    'There is something that is not a number in here.')
                return
        num = int(round(num))
        await ctx.send('Difference: {0}'.format(num))

    #Command multiply, finds the product of all argumant numbers togethers. Rounds to nearest int.
    @bot.command(pass_context=True)
    async def multiply(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("You didn't input anything to multiply.")
            return
        num = 1.0
        for number in args:
            try:
                num *= float(number)
            except ValueError:
                await ctx.send(
                    'There is something that is not a number in here.')
                return
        num = int(round(num))
        await ctx.send('Product: {0}'.format(num))

    
    @bot.command(pass_context=True)
    async def divide(self, ctx, num=0.0, *args):
        if len(args) == 0:
            await ctx.send("You didn't input anything to divide.")
            return
        for number in args:
            try:
                num = num / float(number)
                print(num)
            except ValueError:
                await ctx.send(
                    'There is something that is not a number in here.')
                return

        num = int(round(num))
        await ctx.send('Quotient: {0}'.format(num))

        
    # find rational roots for a polynomial with integral coefficients
    @bot.command(pass_context=True)
    async def find_roots(self, ctx, *args):
        polynomial = ''.join(args)
        tokens = polynomial.replace('-', '+-').split('+')
        polynomial = []

        def place_coef(polynomial, coef, exp):
            # extend the coefficients array if needed
            if len(polynomial) <= exp:
                # polynomial.extend([0 for i in range(exp - len(polynomial) + 1)])
                polynomial.extend([0]  * (exp - len(polynomial) + 1))
            polynomial[exp] += coef
            return polynomial
        
        for tok in tokens:
            coef = 0
            exp = 0
            
            # expecting token looks like '{coef}{variable_letter}{exp}'
            tok_split_by_alpha = re.split(r'[a-z]', tok.lower())

            # constant only
            if len(tok_split_by_alpha) == 1:
                coef = int(tok_split_by_alpha[0])
                exp = 0
                polynomial = place_coef(polynomial, coef, exp)
                continue

            # assume format of {coef}x{exp}
            [coef_str, exp_str] = tok_split_by_alpha[:2]
            if coef_str.startswith('-'):
                # for '-x{exp}'
                coef = -1
                if len(coef_str) > 1:
                    # for '{coef}x{exp}' with coef < 0
                    coef *= int(coef_str[1:])
            elif coef_str == '':
                # for 'x{exp}'
                coef = 1
            else:
                # default case (coef > 0)
                coef = int(coef_str)
            # get exponent; covers '{coef}x' and '{coef}x{exp}'
            exp = 1 if exp_str == '' else int(exp_str)
            polynomial = place_coef(polynomial, coef, exp)
            
        # TODO: get rational root candidates, horner's method, output rational roots

        await ctx.send("This feature is not yet finished, "
                       "but here's the coefficients array: "
                       + str(polynomial))
        return


def setup(bot):
    bot.add_cog(Mathy(bot))
