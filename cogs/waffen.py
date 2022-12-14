import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite

maxcap = 4


class Waffen(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    #
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     async with aiosqlite.connect("waffen.db") as db:
    #         await db.execute(
    #             """
    #             CREATE TABLE IF NOT EXISTS waffen (
    #             owner_id INTEGER,
    #             name TEXT,
    #             power INTEGER,
    #             )"""
    #         )

    @slash_command(description="Füge eine Waffe zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920, 1035691541198545026)
    async def add_waffe(self,
                        ctx,
                        member: Option(discord.Member, "Welcher Spieler soll die waffe bekommen"),
                        name: Option(str, "Wie heißst die Waffe?"),
                        power: Option(int, "Wie viel Stärke?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM waffen WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

            if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title="Waffen-Loot :sparkles:",
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            if power < 0:  # Check ob Power  unter null
                embed = discord.Embed(title="Waffen-Loot :sparkles:",
                                      description=f"***Power*** darf nicht negativ sein"
                                                  f"oder? :thinking: ",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            await db.execute(
                "INSERT INTO waffen (owner_id, name, power) VALUES (?, ?, ?)", (member.id, name, power)
            )
            await db.commit()

            embed = discord.Embed(title="Waffen-Loot :sparkles:",
                                  description=f"Spieler {member.mention} hat ***{name}*** mit ***{power}***"
                                              f" :crossed_swords: erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige dein Waffen an!")
    async def waffen_inventar(self, ctx):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT name, power FROM waffen WHERE owner_id = ?""", (ctx.author.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()

                embed = discord.Embed(title="Deine Waffen :crossed_swords:",
                                      color=discord.Color.dark_purple())
                i = 0  # Durchlauf des Arrays - Itemname
                j = 0  # Durchlauf des Arrays - Itestat
                slot = 1
                rows = len(bag)

                if bag == []:
                    embed.add_field(name="404 Waffe not Found",
                                    value="Anscheinend hast garkeine Waffen in deiner Tasche :cry:",
                                    inline=False)
                    await ctx.respond(
                        embed=embed
                    )
                    return

                for rows in bag:
                    itemname = bag[i]  # Durchlauf des Arrays - Itemname
                    itemstat = bag[j]  # Durchlauf des Arrays - Itestat
                    embed.add_field(name=f"Slot {slot}", value=f"Waffe: {itemname[0]} | Schaden + {itemstat[1]}",
                                    inline=False)
                    j += 1
                    i += 1
                    slot += 1

                embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                await ctx.respond(embed=embed)

    @slash_command(description="Gebe einem Mitspieler eine Waffe")
    async def waffen_geben(self, ctx,
                           member: Option(discord.Member, "Welcher Spieler soll die waffe bekommen"),
                           waffe: Option(str, "Wie heißst die Waffe?")):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM waffen WHERE name = ?""", (waffe,)) as cursor:
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

            async with db.execute("""SELECT owner_id FROM waffen WHERE name = ?""", (waffe,)) as cursor:
                owner_tuple = await cursor.fetchall()
                await cursor.close()
                owner = owner_tuple[0]
                if ctx.author.id != owner[0]:
                    notowner = discord.Embed(title="Übergabeübersicht :scales:",
                                            description="Du besitzt diese Waffe nicht oder "
                                                        "sie existiert nicht in deinem Inventar",
                                            color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=notowner
                        )
                    return

            async with db.execute("""SELECT * FROM waffen WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

                if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                    embed = discord.Embed(title="Übergabeübersicht :scales:",
                                          description=f"Der Spieler ***{member.mention}*** kann ***{waffe}*** leider nicht"
                                                      f" mehr in sein Tasche verstauen :weary:",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

            await db.execute(
                "UPDATE waffen SET owner_id = ? WHERE name = ?", (member.id, waffe)
            )
            await db.commit()

            succsesful = discord.Embed(title="Übergabeübersicht :scales:",
                                         description= f"{ctx.author.mention} hat ***{waffe}*** an {member.mention} übergeben.",
                                         color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Waffen(bot))
