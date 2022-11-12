import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite

maxcap = 9

class Rest(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Füge sonstiges Item zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920, 1035691541198545026)
    async def add_rest(self,
                        ctx,
                        member: Option(discord.Member, "Welcher Spieler soll das Item bekommen"),
                        name: Option(str, "Wie heißst das Item?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM rest WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

            if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title="Sonstiges :sparkles:",
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return


            await db.execute(
                "INSERT INTO rest (owner_id, name) VALUES (?, ?)", (member.id, name)
            )
            await db.commit()

            embed = discord.Embed(title="Sonstiges :sparkles:",
                                  description=f"Spieler {member.mention} hat ***{name}*** erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige deine sonstigen Items an!")
    async def rest_inventar(self, ctx):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT name FROM rest WHERE owner_id = ?""", (ctx.author.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()

                embed = discord.Embed(title="Sonstige Items `ICON`",
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
                    embed.add_field(name=f"Slot {slot}", value=f"Item: {itemname[0]} ",
                                    inline=False)
                    i += 1
                    slot += 1

                await ctx.respond(embed=embed)

    @slash_command(description="Gebe einem Mitspieler etwas von Sonstiges xD")
    async def rest_geben(self, ctx,
                           member: Option(discord.Member, "Welcher Spieler soll das Item bekommen"),
                           rest: Option(str, "Wie heißst das Item?")):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM rest WHERE name = ?""", (rest,)) as cursor:
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

            async with db.execute("""SELECT owner_id FROM rest WHERE name = ?""", (rest,)) as cursor:
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

            async with db.execute("""SELECT * FROM rest WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

                if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                    embed = discord.Embed(title="Übergabeübersicht :scales:",
                                          description=f"Der Spieler ***{member.mention}*** kann ***{rest}*** leider nicht"
                                                      f" mehr in sein Tasche verstauen :weary:",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

            await db.execute(
                "UPDATE rest SET owner_id = ? WHERE name = ?", (member.id, rest)
            )
            await db.commit()

            succsesful = discord.Embed(title="Übergabeübersicht :scales:",
                                         description= f"{ctx.author.mention} hat ***{rest}*** an {member.mention} übergeben.",
                                         color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Rest(bot))