import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite


class bankSystem(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("bank.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                wallet INTEGER DEFAULT 0
                )"""
            )

    @slash_command(description="Füge Betrag X zum Konto hinzu")
    async def geben(self,
                   ctx,
                   member: Option(discord.Member, "Wähle einen User"),
                   betrag: Option(str, "Wie viel soll es sein?")):
        async with aiosqlite.connect("bank.db") as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (member.id,)
            )
            await db.execute(
                "UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (betrag, member.id)
            )
            await ctx.respond(
                f"Von {member.mention} wurde {betrag} auf das Konto gezahlt"
            )
            await db.commit()

    @slash_command(description="Nehme Betrag X vom Konto")
    async def nehmen(self,
                     ctx,
                     member: Option(discord.Member, "Wähle einen User"),
                     betrag: Option(str, "Wie viel soll es sein?")):
        async with aiosqlite.connect("bank.db") as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (member.id,)
            )
            await db.execute(
                "UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (betrag, member.id)
            )
            await ctx.respond(
                f"Von {member.mention} wurde {betrag} von dem Konto abgezogen"
            )
            await db.commit()

    @slash_command(description="Zeige dein Kontostand an")
    async def balance(self, ctx):
        async with aiosqlite.connect("bank.db") as db:
            async with db.execute("SELECT wallet FROM users WHERE user_id = ?", (ctx.author.id,)) as cursor:
                betrag = await cursor.fetchone()
                if betrag == 0:
                    await ctx.respond("Tja dein Konto sieht ganz schön leer aus")
                    return

                await ctx.respond(betrag)


def setup(bot):
    bot.add_cog(bankSystem(bot))