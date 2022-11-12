import discord
from discord.ext import commands
from discord.commands import slash_command , Option
import itertools

import aiosqlite

maxcap = float(100)


class Schatz(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self , bot):
        self.bot = bot

    @slash_command(description="Füge einen Schatz zum Spielerinventar hinzu")
    @commands.has_any_role(1035698515512401920 , 1035691541198545026)
    async def add_schatz(self ,
                       ctx ,
                       member: Option(discord.Member , "Welcher Spieler soll den Schatz bekommen") ,
                       name: Option(str , "Wie heißst der Schatz?"),
                       gewicht: Option(float, "Wie schwer ist das Gewicht?")):

        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT gewicht FROM schatz WHERE owner_id = ?""" , (member.id ,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                weight = itertools.chain(*bag)

            if sum(weight) + gewicht > maxcap:  # Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title="Sonstiges :sparkles:" ,
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:" ,
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            await db.execute(
                "INSERT INTO schatz (owner_id, name, gewicht) VALUES (?, ?, ?)" , (member.id , name, gewicht)
            )
            await db.commit()

            embed = discord.Embed(title="Sonstiges :sparkles:" ,
                                  description=f"Spieler {member.mention} hat ***{name}*** mit einen Gewicht von ***{gewicht} kg*** erhalten" ,
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige deine Schätze an!")
    async def schatz_inventar(self , ctx):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT name FROM schatz WHERE owner_id = ?""" , (ctx.author.id ,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()

                embed = discord.Embed(title="Schatz-Loot `ICON`" ,
                                      color=discord.Color.dark_purple())
                i = 0  # Durchlauf des Arrays - Itemname
                slot = 1
                rows = len(bag)

                if not bag:
                    embed.add_field(name="404 Schatz not Found" ,
                                    value="Anscheinend hast du garkeine Schätze in deiner Tasche :cry:" ,
                                    inline=False)
                    await ctx.respond(
                        embed=embed
                    )
                    return

                for rows in bag:
                    itemname = bag[i]  # Durchlauf des Arrays - Itemname
                    embed.add_field(name=f"Slot {slot}" , value=f"Schatz: {itemname[0]} " ,
                                    inline=False)
                    i += 1
                    slot += 1

                await ctx.respond(embed=embed)

    @slash_command(description="Gebe einem Mitspieler etwas von Sonstiges xD")
    async def schatz_geben(self , ctx ,
                           member: Option(discord.Member , "Welcher Spieler soll den Schatz bekommen") ,
                           name: Option(str , "Wie heißst der Schatz?")):
        async with aiosqlite.connect("inventory.db") as db:
            async with db.execute("""SELECT * FROM schatz WHERE name = ?""" , (name ,)) as cursor:
                item = await cursor.fetchall()
                await cursor.close()
                if not item:  # Check ob Item vorhanden in DB
                    failure = discord.Embed(title="Übergabeübersicht :scales:" ,
                                            description="Ich glaube du hast dich verschrieben! Schau nochmal nach..." ,
                                            color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=failure
                    )
                    return

            async with db.execute("""SELECT owner_id FROM schatz WHERE name = ?""" , (name ,)) as cursor:
                owner_tuple = await cursor.fetchall()
                await cursor.close()
                owner = owner_tuple[0]
                if ctx.author.id != owner[0]:
                    notowner = discord.Embed(title="Übergabeübersicht :scales:" ,
                                             description="Du besitzt diesen Schatz nicht oder "
                                                         "er existiert nicht in deinem Inventar" ,
                                             color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=notowner
                    )
                    return

            async with db.execute("""SELECT * FROM schatz WHERE owner_id = ?""" , (member.id ,)) as cursor:
                bag = await cursor.fetchall()
                await cursor.close()
                countinv = len(bag)

                if countinv > maxcap:  # Check ob das Inventarcap erreicht ist
                    embed = discord.Embed(title="Übergabeübersicht :scales:" ,
                                          description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                      f" mehr in sein Tasche verstauen :weary:" ,
                                          color=discord.Color.dark_purple())
                    await ctx.respond(
                        embed=embed
                    )
                    return

            await db.execute(
                "UPDATE schatz SET owner_id = ? WHERE name = ?" , (member.id , name)
            )
            await db.commit()

            succsesful = discord.Embed(title="Übergabeübersicht :scales:" ,
                                       description=f"{ctx.author.mention} hat ***{name}*** an {member.mention} übergeben." ,
                                       color=discord.Color.dark_purple())
            await ctx.respond(
                embed=succsesful
            )


def setup(bot):
    bot.add_cog(Schatz(bot))
