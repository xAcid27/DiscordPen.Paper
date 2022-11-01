import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite

coin = "<a:BerryCoin:1036423419543166986>"  # :BerryCoin: Emoji Integration
note = "<a:BerryNote:1036443156230717510>"  # :BerryNote: Emoji Integration

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
                   betrag: Option(int, "Wie viel soll es sein?")):
        async with aiosqlite.connect("bank.db") as db:
            async with db.execute("""SELECT wallet FROM users WHERE user_id = ?""", (ctx.author.id,)) as cursor:
                guthaben = await cursor.fetchone()
            if betrag < 0:  # Abfrage ob der abgezogene Betrag als 0 zum klauen
                embed = discord.Embed(title="Transaktion",
                                      description=f"{member.mention} du kannst keine ***{betrag}*** {coin} geben",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return
            if betrag > guthaben[0]:#Check ob User genug Geld hat
                if guthaben[0] < 1000:#EmiojiCheck
                    embed = discord.Embed(title="Transaktion",
                                          description=f"{ctx.author.mention} du hast nur ***{guthaben[0]}*** {coin} in der Tasche",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return
                else:
                    embed = discord.Embed(title="Transaktion",
                                          description=f"{member.mention} du hast nur ***{guthaben[0]}*** {note} in der Tasche",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return
            if betrag >= 1000: #EmojiCheck
                embed = discord.Embed(title="Transaktion",
                                      description=f"{ctx.author.mention} hat {member.mention}  ***{betrag}*** {note} "
                                                  f"geschenkt, was ein Ehrenmann :sparkles:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
            else:
                embed = discord.Embed(title="Transaktion",
                                      description=f"{ctx.author.mention} hat {member.mention}  ***{betrag}*** {coin} "
                                                  f"geschenkt, was ein Ehrenmann :sparkles:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )

            await db.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (member.id,)
            )
            await db.execute(
                "UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (betrag, member.id)
            )
            await db.execute(
                "UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (betrag, ctx.author.id)
            )
            await db.commit()

    @slash_command(description="Füge Betrag X zum Konto hinzu")
    async def add(self,
                   ctx,
                   member: Option(discord.Member, "Wähle einen User"),
                   betrag: Option(int, "Wie viel soll es sein?")):
        async with aiosqlite.connect("bank.db") as db:
            if betrag < 0:  # Abfrage ob der abgezogene Betrag als 0 zum klauen
                embed = discord.Embed(title="Transaktion",
                                      description=f"Du kannst {member.mention} keine ***{betrag}*** {coin} geben ",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return
            if betrag >= 1000:  # EmojiCheck
                embed = discord.Embed(title="Transaktion",
                                      description=f"***Der Spielleiter*** hat {member.mention}  ***{betrag}*** {note} "
                                              f"geschenkt, was ein Ehrenmann :sparkles:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
            else:
                embed = discord.Embed(title="Transaktion",
                                      description=f"***Der Spielleiter*** hat {member.mention}  ***{betrag}*** {coin} "
                                                  f"geschenkt, was ein Ehrenmann :sparkles:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                await db.commit()

            await db.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (member.id,)
            )
            await db.execute(
                "UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (betrag, member.id)
            )



    @slash_command(description="Nehme Betrag X vom Konto")
    async def lose(self,
                     ctx,
                     member: Option(discord.Member, "Wähle einen User"),
                     betrag: Option(int, "Wie viel soll es sein?")):
        async with aiosqlite.connect("bank.db") as db:
            async with db.execute("""SELECT wallet FROM users WHERE user_id = ?""", (member.id,)) as cursor:
                guthaben = await cursor.fetchone()
                if guthaben[0] < betrag:  # Abfrage ob der abgezogene Betrag größer als guthaben ist
                    if betrag < 1000:
                        embed = discord.Embed(title="Transaktion",
                                              description=f"{member.mention} hat keine ***{betrag}*** {coin} auf dem Konto",
                                              color=discord.Color.dark_purple())
                        await ctx.respond(
                            embed=embed
                        )
                        return
                    else:
                        embed = discord.Embed(title="Transaktion",
                                              description=f"{member.mention} hat keine ***{betrag}*** {note} auf dem Konto",
                                              color=discord.Color.dark_purple())
                        await ctx.respond(
                            embed=embed
                        )
                        return

                if betrag < 0:  # Kein Minusgeld schenken

                    embed = discord.Embed(title="Transaktion",
                                          description=f"Du kannst von {member.mention} keine ***{betrag}*** {coin} vom dem Konto abziehen",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

                if betrag < 1000:  # Emojicheck
                    embed = discord.Embed(title="Transaktion",
                                          description=f"***Der Spielleiter*** sagt {member.mention} hat ***{betrag}*** {coin} verloren",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                else:
                    embed = discord.Embed(title="Transaktion",
                                          description=f"***Der Spielleiter*** sagt {member.mention} hat ***{betrag}*** {note} verloren",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )

            await db.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (member.id,)
            )
            await db.execute(
                "UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (betrag, member.id)
            )
            await db.commit()

    @slash_command(description="Zeige dein Kontostand an")
    async def balance(self, ctx):
        async with aiosqlite.connect("bank.db") as db:
            async with db.execute("""SELECT wallet FROM users WHERE user_id = ?""", (ctx.author.id,)) as cursor:
                guthaben = await cursor.fetchone()
                if guthaben is None:
                    await ctx.respond("Anscheinend hast du noch kein Konto :octagonal_sign: ")
                    return
                if guthaben[0] < 1000:
                    embed = discord.Embed(title="Dein Kontostand",
                                          description=f"Deine aktuelle Beute liegt bei ***{guthaben[0]}*** {coin}",
                                          color=discord.Color.dark_purple())

                    await ctx.respond(
                        embed=embed
                    )
                else:
                    embed = discord.Embed(title="Dein Kontostand",
                                          description=f"Deine aktuelle Beute liegt bei ***{guthaben[0]}*** {note}",
                                          color=discord.Color.dark_purple())

                    await ctx.respond(
                        embed=embed
                    )
def setup(bot):
    bot.add_cog(bankSystem(bot))