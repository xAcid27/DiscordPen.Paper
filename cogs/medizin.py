import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite

maxcap = 9
hpemoji ="<:hp:1041131183108522006>"

class Medizin(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Füge Medizin zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920, 1035691541198545026)
    async def add_medizin(self,
                        ctx,
                        member: Option(discord.Member, "Welcher Spieler soll die Medizin bekommen"),
                        name: Option(str, "Wie heißst die Medizin?"),
                        heal: Option(int, "Wie viel Stärke?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM medizin WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

            if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title="Loot :sparkles:",
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            if heal < 0:  # Check ob Heal  unter null
                embed = discord.Embed(title="Loot :sparkles:",
                                      description=f"***Heal*** darf nicht negativ sein"
                                                  f"oder? :thinking: ",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            await db.execute(
                "INSERT INTO medizin (owner_id, name, heal) VALUES (?, ?, ?)", (member.id, name, heal)
            )
            await db.commit()

            embed = discord.Embed(title="Medizin-Loot :hospital:",
                                  description=f"Spieler {member.mention} hat ***{name}*** mit ***{heal}***"
                                              f" {hpemoji} erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Gebe einem Mitspieler eine Medizin")
    async def medizin_geben(self, ctx,
                           member: Option(discord.Member, "Welcher Spieler soll die medizin bekommen"),
                           medizin: Option(str, "Wie heißst die medizin?")):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM medizin WHERE name = ?""", (medizin,)) as cursor:
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

            async with db.execute("""SELECT owner_id FROM medizin WHERE name = ?""", (medizin,)) as cursor:
                owner_tuple = await cursor.fetchall()
                await cursor.close()
                owner = owner_tuple[0]
                if ctx.author.id != owner[0]:
                    notowner = discord.Embed(title="Übergabeübersicht :scales:",
                                            description="Du besitzt diese Medizin nicht oder "
                                                        "sie existiert nicht in deinem Inventar",
                                            color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=notowner
                        )
                    return

            async with db.execute("""SELECT * FROM medizin WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

                if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                    embed = discord.Embed(title="Übergabeübersicht :scales:",
                                          description=f"Der Spieler ***{member.mention}*** kann ***{medizin}*** leider nicht"
                                                      f" mehr in sein Tasche verstauen :weary:",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

            await db.execute(
                "UPDATE medizin SET owner_id = ? WHERE name = ?", (member.id, medizin)
            )
            await db.commit()

            succsesful = discord.Embed(title="Übergabeübersicht :scales:",
                                         description= f"{ctx.author.mention} hat ***{medizin}*** an {member.mention} übergeben.",
                                         color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Medizin(bot))