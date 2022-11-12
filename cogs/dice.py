import discord
from discord.ext import commands
from discord.commands import slash_command , Option
import aiosqlite


class Dice(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self , bot):
        self.bot = bot

    @slash_command()
    async def dice(self, ctx,):
        dice4 = ["1", "2", "3", "4"]
        dice6 = ["1", "2", '3', "4", "5", "6"]
        dice8 = ["1", "2", "3", "4", "5", "6", "7", "8"]
        dice10 = ["1", "2", "3", "4",  "5", "6",  "7", "8", "9", "10"]
        dice12 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        dice20 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                  "17", "18", "19", "20"]

        message = await ctx.send(
            "Welcher Würfel darf es denn sein?",
        )





def setup(bot):
    bot.add_cog(Dice(bot))
