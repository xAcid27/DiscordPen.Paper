import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import aiosqlite

maxcap = 4


class Waffen(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Füge eine Waffe zum Spielerinventar hinzu")
    async def add_waffe(self,
                        ctx,
                        member: Option(discord.Member, "Welcher Spieler soll die waffe bekommen"),
                        name: Option(str, "Wie heißst die Waffe?"),
                        power: Option(int, "Wie viel Stärke?"),
                        magie: Option(int, "Wie viel Magie?")):

        async with aiosqlite.connect("waffen.db") as db:
            async with db.execute("""SELECT * FROM waffen WHERE owner_id = ?""", (member.id,)) as cursor:
                all = await cursor.fetchall()
                countinv = len(all)

            if countinv > maxcap:#Check ob das Inventarcap erreicht ist
                embed = discord.Embed(title="Loot :sparkles:",
                                      description=f"Der Spieler ***{member.mention}*** kann ***{name}*** leider nicht"
                                                  f" mehr in sein Tasche verstauen :weary:",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            if power | magie < 0:#Check ob Power oder Magie unter null
                embed = discord.Embed(title="Loot :sparkles:",
                                      description=f"***Power*** und ***Magie*** dürfen nicht negativ sein"
                                                  f"oder? :thinking: ",
                                      color=discord.Color.dark_purple())
                await ctx.respond(
                    embed=embed
                )
                return

            await db.execute(
                "INSERT INTO waffen (owner_id, name, power, magie) VALUES (?, ?, ?, ?)", (member.id, name, power, magie,)
            )
            await db.commit()

            embed = discord.Embed(title="Loot :sparkles:",
                                  description=f"Spieler {member.mention} hat ***{name}*** mit ***{power}***"
                                              f" :crossed_swords: und mit ***{magie}*** :zap: erhalten",
                                  color=discord.Color.dark_purple())

            await ctx.respond(
                embed=embed
            )

    @slash_command(description="Zeige dein Waffen an!")
    async def waffen_inventar(self, ctx):
        async with aiosqlite.connect("waffen.db") as db:
            async with db.execute("""SELECT name, power, magie FROM waffen WHERE owner_id = ?""",
                                  (ctx.author.id,)) as cursor:
                all = await cursor.fetchall
                rows = len(all)

                for rows in all:
                     ctx.respond("Item: ", all[0])
                     ctx.respond("Power: ", all[1])
                     ctx.respond("Magie: ", all[2])

    # @slash_command(description="How Much?")
    # async def howmuch(self, ctx, member: Option(discord.Member, "Member")):
    #     async with aiosqlite.connect("waffen.db") as db:


def setup(bot):
    bot.add_cog(Waffen(bot))