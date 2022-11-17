import asyncio

import discord
import itertools

from discord import Interaction
from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton
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

    @slash_command()
    async def example(self, ctx):
        menu = ViewMenu(ctx , menu_type=ViewMenu.TypeEmbed)

        for member in ctx.guild.members:
            if member.avatar:
                embed = discord.Embed(description=f'Joined {member.joined_at.strftime("%b. %d, %Y")}')
                embed.set_author(name=member.name , icon_url=member.avatar.url)
                menu.add_page(embed)

        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.end_session())

        await menu.start()


        # https: // github.com / Defxult / reactionmenu

        # @commands.Cog.listener
        # async def on_raw_reaction_add(payload):
        #     if payload.message_id == message_id:
        #         if payload.emoji_id == emojilist[1]:
        #             await ctx.respond("Deine Waffen Diggi ")





def setup(bot):
    bot.add_cog(Inventar(bot))
