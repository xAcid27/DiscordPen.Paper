import asyncio

import discord
import itertools

from discord import Interaction
from discord.ext import commands
from discord.commands import slash_command , Option
import aiosqlite


def convert_tup(tup):
    str = ""
    for item in tup:
        str = str + item
    return str


emojilist = ["⚔" , "<:hp:1041131183108522006>" , '🍔' , "<:schatze:1041119880839172166>" ,
             "🔨" , "<:sonst:1041129534730281081>", "❌"]

inventartup = ["Waffen:crossed_swords: | " , f"Medizin {emojilist[1]} | " , "Nahrung :hamburger: | " ,
               f"Schätze {emojilist[3]} | " , "Crafting :hammer: | " , f"Sonstiges {emojilist[5]}"]

inventarover = convert_tup(inventartup)


class Inventar(commands.Cog):
    def __init__(self , bot):
        self.bot = bot


    @slash_command(description="Zeige dein Inventar an!")
    async def inventar(self , ctx):
        invoverlay = discord.Embed(title="Dein Inventar :school_satchel:" ,
                                   description="In welche Tasche möchstest hinein schauen? \n" ,
                                   color=discord.Color.dark_purple())

        invoverlay.add_field(name="Taschen" , value=f"{inventarover}")

        msg = await ctx.respond(
            embed=invoverlay
        )

        y = 0
        for i in emojilist:
            await ctx.message.add_reaction(emojilist[y])
            y += 1

        message_id = await ctx.channel.fetch_message(msg)  # Cache Message
        return

        # https: // github.com / Defxult / reactionmenu

        # @commands.Cog.listener
        # async def on_raw_reaction_add(payload):
        #     if payload.message_id == message_id:
        #         if payload.emoji_id == emojilist[1]:
        #             await ctx.respond("Deine Waffen Diggi ")





def setup(bot):
    bot.add_cog(Inventar(bot))
