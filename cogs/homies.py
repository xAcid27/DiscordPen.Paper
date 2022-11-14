import itertools

import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite


class Homies(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Füge sonstiges Item zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920, 1035691541198545026)
    async def add_homie(self,
                        ctx,
                        member: Option(discord.Member, "Welcher Spieler soll das Item bekommen", ),
                        name: Option(str, "Wie heißst das Item?"),
                        anzahl: Option(int, "Wie heißt der Homie?", required=False)):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM homies WHERE owner_id = ?""", (member.id,)) as cursor:
                bagtup = await cursor.fetchall()
                await cursor.close()

                async with db.execute("""SELECT amount FROM homies WHERE name = ?""", (name,)) as cursor:
                    amounttup = await cursor.fetchall()
                    await cursor.close()

                bag = itertools.chain(*bagtup)

            if anzahl is None:
                anzahl = 1

            amount = (sum([item[0] for item in amounttup]) + anzahl)

            if name in list(bag):
                await db.execute(
                    "UPDATE homies SET amount = ? WHERE name = ? AND owner_id = ?", (amount, name, member.id)
                )
            else:
                await db.execute(
                 "INSERT INTO homies (owner_id, name, amount) VALUES (?, ?, ?)", (member.id, name, anzahl)
                )

            await db.commit()

            embed = discord.Embed(title="Sonstiges :sparkles:",
                                  description=f"Spieler {member.mention} hat den Homie ***{name} {anzahl}x*** erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige deine sonstigen Items an!")
    async def homies_inventar(self, ctx):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT name, amount FROM homies WHERE owner_id = ?""", (ctx.author.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()

                embed = discord.Embed(title=" Deine Homies `ICON`",
                                      color=discord.Color.dark_purple())
                i = 0  # Durchlauf des Arrays - Itemname
                slot = 1
                rows = len(bag)

                if not bag:
                    embed.add_field(name="404 Item not Found",
                                    value="Anscheinend hast du garkeine Sonstigen Items in deiner Tasche :cry:",
                                    inline=False)
                    await ctx.respond(
                        embed=embed
                    )
                    return

                for rows in bag:
                    itemname = bag[i]  # Durchlauf des Arrays - Itemname
                    embed.add_field(name=f"Slot {slot}", value=f"Item: ***{itemname[0]} {itemname[1]}x***",
                                    inline=False)
                    i += 1
                    slot += 1

                # embed.set_footer(text=f"Verfübare Slots: {abs(maxcap-i) + 1}")

                await ctx.respond(embed=embed)

    @slash_command(description="Übertrage einen Spieler dein Homie")
    async def homies_geben(self, ctx,
                           member: Option(discord.Member, "Welcher Spieler soll das Item bekommen"),
                           homie: Option(str, "Welcher Homie soll es sein?"),
                           anzahl: Option(int, "Wie viele von deinen Homies?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM homies WHERE name = ?""", (homie,)) as cursor:
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

            async with db.execute("""SELECT owner_id FROM homies WHERE name = ?""", (homie,)) as cursor:
                owner_tuple = await cursor.fetchall()
                await cursor.close()
                owner = owner_tuple[0]
                if ctx.author.id != owner[0]:
                    notowner = discord.Embed(title="Übergabeübersicht :scales:",
                                            description="Du besitzt dieses Item nicht oder "
                                                        "sie existiert nicht in deinem Inventar",
                                            color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=notowner
                        )
                    return

            # async with db.execute("""SELECT * FROM homies WHERE owner_id = ?""", (member.id,)) as cursor:
            #     bag = await cursor.fetchall()
            #     await cursor.close()
            #     countinv = len(bag)
            #
            #     if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
            #         embed = discord.Embed(title="Übergabeübersicht :scales:",
            #                               description=f"Der Spieler ***{member.mention}*** kann ***{rest}*** leider nicht"
            #                                           f" mehr in sein Tasche verstauen :weary:",
            #                               color=discord.Color.dark_purple())
            #         await ctx.respond(
            #             embed=embed
            #         )
            #         return

            async with db.execute("""SELECT amount FROM homies WHERE name = ? AND owner_id = ? """, (homie, ctx.author.id)) as cursor:
                amounttup = await cursor.fetchall()
                await cursor.close()

                updateamount = (sum([item[0] for item in amounttup]) - anzahl)


                await db.execute(
                    "UPDATE homies SET amount = ? WHERE name = ?", (updateamount, homie)
                )

                await db.execute(
                    "INSERT INTO homies (owner_id, name, amount) VALUES (?, ?, ?)", (member.id, homie, anzahl)
                )
                await db.commit()


            succsesful = discord.Embed(title="Übergabeübersicht :scales:",
                                         description= f"{ctx.author.mention} hat ***{homie}*** an {member.mention} übergeben.",
                                         color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Homies(bot))