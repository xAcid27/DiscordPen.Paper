import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite

maxcap = 4

class Nahrung(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Füge Nahrung zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920, 1035691541198545026)
    async def add_nahrung(self,
                        ctx,
                        member: Option(discord.Member, "Welcher Spieler soll die Nahrung bekommen"),
                        name: Option(str, "Wie heißst die Nahrung?"),
                        hp: Option(int, "Wie viel HP werden hergesellt?"),
                        sp: Option(int, "Wie viel SP verden hergestellt?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM nahrung WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

            if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title="Nahrungs-Loot :sparkles:",
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            if hp < 0 or sp < 0:  # Check ob Heal  unter null
                embed = discord.Embed(title="Nahrungs-Loot :sparkles:",
                                      description=f"***HP*** und ***SP*** dürfen nicht negativ sein"
                                                  f"oder? :thinking: ",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            await db.execute(
                "INSERT INTO nahrung (owner_id, name, hp, sp) VALUES (?, ?, ?, ?)", (member.id, name, hp, sp)
            )
            await db.commit()

            embed = discord.Embed(title="Nahrungs-Loot :sparkles:",
                                  description=f"Spieler {member.mention} hat ***{name}***  mit ***{hp} HP***"
                                              f" :hamburger: und ***{sp} SP*** `(hier sollte ein ICON hin)`  erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige dein Nahrung an!")
    async def nahrung_inventar(self, ctx):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT name, hp, sp FROM nahrung WHERE owner_id = ?""", (ctx.author.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()

                embed = discord.Embed(title="Deine Nahrung :hamburger:",
                                      color=discord.Color.dark_purple())
                i = 0  # Durchlauf des Arrays - Itemname
                j = 0  # Durchlauf des Arrays - Itestat
                k = 0  # Durchlauf des Array -Itemstat 2
                slot = 1
                rows = len(bag)

                if not bag:
                    embed.add_field(name="404 Nahrung not Found",
                                    value="Anscheinend hast du garkeine Nahrung in deiner Tasche :cry:",
                                    inline=False)
                    await ctx.respond(
                        embed=embed
                    )
                    return

                for rows in bag:
                    itemname = bag[i]  # Durchlauf des Arrays - Itemname
                    itemstat = bag[j]  # Durchlauf des Arrays - Itestat
                    itemstat2 = bag[k] # Durchlauf des Arrays - Itestat 2
                    embed.add_field(name=f"Slot {slot}", value=f"Nahrung: {itemname[0]} | HP + {itemstat[1]} | SP + {itemstat2[2]}",
                                    inline=False)
                    j += 1
                    i += 1
                    k += 1
                    slot += 1

                embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                await ctx.respond(embed=embed)

    @slash_command(description="Gebe einem Mitspieler etwas von der Nahrung")
    async def nahrung_geben(self, ctx,
                           member: Option(discord.Member, "Welcher Spieler soll die Nahrung bekommen"),
                           nahrung: Option(str, "Wie heißst die Nahrung?")):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM nahrung WHERE name = ?""", (nahrung,)) as cursor:
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

            async with db.execute("""SELECT owner_id FROM nahrung WHERE name = ?""", (nahrung,)) as cursor:
                owner_tuple = await cursor.fetchall()
                await cursor.close()
                owner = owner_tuple[0]
                if ctx.author.id != owner[0]:
                    notowner = discord.Embed(title="Übergabeübersicht :scales:",
                                            description="Du besitzt diese nahrung nicht oder "
                                                        "sie existiert nicht in deinem Inventar",
                                            color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=notowner
                        )
                    return

            async with db.execute("""SELECT * FROM nahrung WHERE owner_id = ?""", (member.id,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

                if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                    embed = discord.Embed(title="Übergabeübersicht :scales:",
                                          description=f"Der Spieler ***{member.mention}*** kann ***{nahrung}*** leider nicht"
                                                      f" mehr in sein Tasche verstauen :weary:",
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

            await db.execute(
                "UPDATE nahrung SET owner_id = ? WHERE name = ?", (member.id, nahrung)
            )
            await db.commit()

            succsesful = discord.Embed(title="Übergabeübersicht :scales:",
                                         description= f"{ctx.author.mention} hat ***{nahrung}*** an {member.mention} übergeben.",
                                         color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Nahrung(bot))