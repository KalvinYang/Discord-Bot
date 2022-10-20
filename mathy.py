#Discord imports allow for easy access to connection to discord and making commands.
import discord
from discord.ext import commands

import re
import itertools
from fractions import Fraction

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

        # evaluate polynomial at x using synthetic division
        def evaluate(polynomial, x):
            acc = Fraction(polynomial[-1]) # accumulator
            result = [acc]
            assert len(polynomial) > 0, "cannot evaluate empty expression"
            if len(polynomial) < 2:
                return acc, result
            for i in polynomial[-2::-1]:
                acc = (acc * x) + Fraction(i)
                result.append(acc)
            return acc, result[-2::-1]

        # negative values count!
        def factorize(x):
            if x < Fraction(0):
                x *= Fraction(-1, 1)
            n_positive_factors = [i for i in range(1, x.numerator + 1) if x.numerator % i == 0]
            n_negative_factors = list(map(lambda n: -n, n_positive_factors))
            d_positive_factors = [i for i in range(1, x.denominator + 1) if x.denominator % i == 0]
            d_negative_factors = list(map(lambda n: -n, d_positive_factors))
            return [Fraction(a, b)
                    for a, b in itertools.product(
                        n_positive_factors + n_negative_factors,
                        d_positive_factors + d_negative_factors)]
            
        roots = []

        # if 0 is a root, eliminate it now
        while polynomial[0] == 0:
            polynomial = polynomial[1:]
            roots.append(Fraction(0))

        while len(polynomial) > 1:
            ps = factorize(polynomial[0])
            qs = factorize(polynomial[-1])
            found_a_root = False
            candidates = []
            # Fractions are not hashable, so we can't use set() :(
            for p in ps:
                for q in qs:
                    candidate = Fraction(p, q)
                    if candidate not in candidates:
                        candidates.append(candidate)
            for candidate in candidates:
                remainder, quotient = evaluate(polynomial, candidate)
                if remainder == 0:
                    found_a_root = True
                    polynomial = quotient
                    roots.append(candidate)
                    break
            if not found_a_root:
                break

        # at this point polynomial may look something like this:
        # [1, 0, 1]
        # the index indicates the power
        # value in list would be the coefficients
        # only print the remaining polynomial if len(polynomial) > 2
        
        await ctx.send(f"Rational roots for polynomial: {roots}")
        return


def setup(bot):
    bot.add_cog(Mathy(bot))