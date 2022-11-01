import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import aiosqlite


class Inventory(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("inventory.db") as db:
            await db.execute(
                """
                CREATE TABLE inventory (
	            user_id INTEGER PRIMARY KEY,
	            Waffen	TEXT,
	            Schätze	TEXT,
	            Crafting TEXT,
	            Medizin  TEXT,
	            Nahrung TEXT,
	            Sonstiges TEXT
	            )"""
            )


def setup(bot):
    bot.add_cog(Inventory(bot))
