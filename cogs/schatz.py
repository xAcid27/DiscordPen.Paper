import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import itertools

import aiosqlite

maxcap = float(100)
emoji = "<:schatze:1041072838150467615>"


class Schatz(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Füge einen Schatz zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920, 1035691541198545026)
    async def add_schatz(self,
                         ctx,
                         member: Option(discord.Member, "Welcher Spieler soll den Schatz bekommen"),
                         name: Option(str, "Wie heißst der Schatz?"),
                         gewicht: Option(float, "Wie schwer ist das Gewicht?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT gewicht FROM schatz WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                weight = itertools.chain(*bag)

            if sum(weight) + gewicht > maxcap:  # Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title=f"Schatz-Loot {emoji}",
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            await db.execute(
                "INSERT INTO schatz (owner_id, name, gewicht) VALUES (?, ?, ?)", (member.id, name, gewicht)
            )
            await db.commit()

            embed = discord.Embed(title=f"Schatz-Loot {emoji}",
                                  description=f"Spieler {member.mention} hat ***{name}*** mit einen Gewicht von ***{gewicht} kg*** erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige deine Schätze an!")
    async def schatz_inventar(self, ctx):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT name, gewicht FROM schatz WHERE owner_id = ?""",
                                  (ctx.author.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()

                embed = discord.Embed(title=f"Schatz-Loot {emoji}",
                                      color=discord.Color.dark_purple())
                i = 0  # Durchlauf des Arrays - Itemname
                slot = 1
                rows = len(bag)

                if not bag:
                    embed.add_field(name="404 Schatz not Found",
                                    value="Anscheinend hast du garkeine Schätze in deiner Tasche :cry:",
                                    inline=False)
                    await ctx.respond(
                        embed=embed
                    )
                    return

                for rows in bag:
                    itemname = bag[i]  # Durchlauf des Arrays - Itemname
                    itemstat = bag[i]  # Durchlauf des Arrays - Itemstat
                    embed.add_field(name=f"Slot {slot}", value=f"***{itemname[0]}*** mit "
                                                               f"einem Gewicht von ***{itemstat[1]}*** kg ",
                                    inline=False)
                    i += 1
                    slot += 1

                async with db.execute("""SELECT gewicht FROM schatz WHERE owner_id = ?""",
                                      (ctx.author.id,)) as cursor:
                    gewichttup = await cursor.fetchall()
                    gewicht = itertools.chain(*gewichttup)
                    await cursor.close()

                embed.set_footer(text=f"Verfübares Gewicht: {abs(maxcap - sum(gewicht))}kg")

                await ctx.respond(embed=embed)

    @slash_command(description="Gebe einem Mitspieler etwas von Sonstiges xD")
    async def schatz_geben(self, ctx,
                           member: Option(discord.Member, "Welcher Spieler soll den Schatz bekommen"),
                           name: Option(str, "Wie heißst der Schatz?")):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM schatz WHERE name = ?""", (name,)) as cursor:
                item = await cursor.fetchall()
                await cursor.close()
                if not item:  # Check ob Item vorhanden in DB
                    failure = discord.Embed(title="Übergabeübersicht :scales:",
                                            description="Ich glaube du hast dich verschrieben! Schau nochmal nach...",
                                            color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=failure
                    )
                    return

            async with db.execute("""SELECT owner_id FROM schatz WHERE name = ?""", (name,)) as cursor:
                owner_tuple = await cursor.fetchall()
                await cursor.close()
                owner = owner_tuple[0]
                if ctx.author.id != owner[0]:
                    notowner = discord.Embed(title="Übergabeübersicht :scales:",
                                             description="Du besitzt diesen Schatz nicht oder "
                                                         "er existiert nicht in deinem Inventar",
                                             color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=notowner
                    )
                    return

            async with db.execute("""SELECT gewicht FROM schatz WHERE owner_id = ?""", (member.id,)) as cursor:
                gewichttup = await cursor.fetchall()
                await cursor.close()
            async with db.execute("""SELECT gewicht FROM schatz WHERE name = ?""", (name,)) as cursor:
                itemgewichttup = await cursor.fetchall()
                await cursor.close()

                gewicht = itertools.chain(*gewichttup)
                itemgewicht = itertools.chain(*itemgewichttup)

                if sum(gewicht) + sum(itemgewicht) > maxcap:  # Check ob das Inventarcap erreicht ist
                    embed = discord.Embed(title="Übergabeübersicht :scales:",
                                          description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                      f" mehr in sein Tasche verstauen :weary:",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

            await db.execute(
                "UPDATE schatz SET owner_id = ? WHERE name = ?", (member.id, name)
            )
            await db.commit()

            succsesful = discord.Embed(title="Übergabeübersicht :scales:",
                                       description=f"{ctx.author.mention} hat ***{name}*** an {member.mention} übergeben.",
                                       color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Schatz(bot))
