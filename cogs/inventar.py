import asyncio, discord, aiosqlite, itertools
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ui import Select, View


def convert_tup(tup):
    str = ""
    for item in tup:
        str = str + item
    return str


emojilist = ["⚔", "<:hp:1041131183108522006>", "<:sp:1041124851647266918>", '🍔', "<:schatze:1041119880839172166>",
             "🔨", "<:sonst:1041129534730281081>", "❌"]

inventartup = ["Waffen", "Medizin", "Nahrung",
               "Schätze", "Crafting", "Sonstiges", "Close"]


class Inventar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def taschen(self, ctx):
        await ctx.respond(
            f"Deine Taschen {ctx.author.mention}",
            view=SelectView(),
            delete_after=60
        )


class SelectView(discord.ui.View):
    @discord.ui.select(
        placeholder="Wähle deine Tasche",
        options=[
            discord.SelectOption(
                label=f"{inventartup[0]}",
                emoji=f"{emojilist[0]}",
                description=f"Deine {inventartup[0]}"
            ),

            discord.SelectOption(
                label=f"{inventartup[1]}",
                emoji=f"{emojilist[1]}",
                description=f"Deine {inventartup[1]}"
            ),

            discord.SelectOption(
                label=f"{inventartup[2]}",
                emoji=f"{emojilist[3]}",
                description=f"Deine {inventartup[2]}"
            ),

            discord.SelectOption(
                label=f"{inventartup[3]}",
                emoji=f"{emojilist[4]}",
                description=f"Deine {inventartup[3]}"
            ),

            discord.SelectOption
            (label=f"{inventartup[4]}",
             emoji=f"{emojilist[5]}",
             description=f"Deine {inventartup[4]}"
             ),

            discord.SelectOption(
                label=f"{inventartup[5]}",
                emoji=f"{emojilist[6]}",
                description=f"Deine {inventartup[5]}"
            ),

            discord.SelectOption(
                label=f"{inventartup[6]}",
                emoji=f"{emojilist[7]}",
                description=f"{inventartup[6]} Inventar"
            )
        ])
    async def select_callbback(self, select, interaction):
        if "Waffen" in interaction.data["values"]:
            async with aiosqlite.connect("inventory.db") as db:
                async with db.execute("""SELECT name, power FROM waffen WHERE owner_id = ?""",
                                      (interaction.user.id,)) as cursor:

                    bag = await cursor.fetchall()
                    await cursor.close()

                    embed = discord.Embed(
                        title="Deine Waffen :crossed_swords:",
                        color=discord.Color.dark_purple()
                    )

                    maxcap = 4
                    i = 0  # Durchlauf des Arrays - Itemname
                    j = 0  # Durchlauf des Arrays - Itestat
                    slot = 1

                    rows = len(bag)

                    if bag == []:
                        embed.add_field(
                            name="404 Waffe not Found",
                            value="Anscheinend hast garkeine Waffen in deiner Tasche :cry:",
                            inline=False
                        )

                        await interaction.message.edit(
                            content=f"Deine Taschen sind leer {interaction.user.mention}",
                            embed=embed
                        )
                        await interaction.response.defer()
                        return

                    for rows in bag:

                        itemname = bag[i]  # Durchlauf des Arrays - Itemname
                        itemstat = bag[j]  # Durchlauf des Arrays - Itestat

                        embed.add_field(
                            name=f"Slot {slot}",
                            value=f"Waffe: {itemname[0]} | Schaden + {itemstat[1]}",
                            inline=False
                        )

                        j += 1
                        i += 1
                        slot += 1

                    embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                    await interaction.message.edit(
                        content=f"Pass auf die spitzen auf! {interaction.user.mention}",
                        embed=embed,
                        view=SelectView()
                    )
                    await interaction.response.defer()



        if "Medizin" in interaction.data["values"]:
            async with aiosqlite.connect("inventory.db") as db:
                async with db.execute("""SELECT name, heal FROM medizin WHERE owner_id = ?""",
                                      (interaction.user.id,)) as cursor:
                    bag = await cursor.fetchall()
                    await cursor.close()

                    embed = discord.Embed(
                        title="Deine Medizin :medical_symbol:",
                        color=discord.Color.dark_purple()
                    )

                    i = 0  # Durchlauf des Arrays - Itemname
                    j = 0  # Durchlauf des Arrays - Itestat
                    maxcap = 9

                    slot = 1
                    rows = len(bag)

                    if not bag:
                        embed.add_field(
                            name="404 Medizin not Found",
                            value="Anscheinend hast du garkeine Medizin in deiner Tasche :cry:",
                            inline=False
                        )

                        await interaction.message.edit(
                            content=f"Deine Taschen sind leer {interaction.user.mention}",
                            embed=embed
                        )
                        await interaction.response.defer()
                        return

                    for rows in bag:
                        itemname = bag[i]  # Durchlauf des Arrays - Itemname
                        itemstat = bag[j]  # Durchlauf des Arrays - Itestat
                        embed.add_field(name=f"Slot {slot}",
                                        value=f"Medizin: {itemname[0]} | HP + {itemstat[1]} {emojilist[2]}",
                                        inline=False)
                        j += 1
                        i += 1
                        slot += 1

                    embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                    await interaction.edit_response(
                        content=f"Damit du wieder auf die Beine kommst! {interaction.user.mention}",
                        embed=embed
                    )
                    await interaction.response.defer()

        if "Nahrung" in interaction.data["values"]:
            async with aiosqlite.connect("inventory.db") as db:
                async with db.execute("""SELECT name, hp, sp FROM nahrung WHERE owner_id = ?""",
                                      (interaction.user.id,)) as cursor:
                    bag = await cursor.fetchall()
                    await cursor.close()

                    embed = discord.Embed(title="Deine Nahrung :hamburger:",
                                          color=discord.Color.dark_purple())

                    maxcap = 4
                    i = 0  # Durchlauf des Arrays - Itemname
                    j = 0  # Durchlauf des Arrays - Itestat
                    k = 0  # Durchlauf des Array -Itemstat 2
                    slot = 1
                    rows = len(bag)

                    if not bag:
                        embed.add_field(name="404 Nahrung not Found",
                                        value="Anscheinend hast du garkeine Nahrung in deiner Tasche :cry:",
                                        inline=False)
                        await interaction.message.edit(
                            content=f"Deine Taschen sind leer {interaction.user.mention}",
                            embed=embed
                        )
                        await interaction.response.defer()
                        return

                    for rows in bag:
                        itemname = bag[i]  # Durchlauf des Arrays - Itemname
                        itemstat = bag[j]  # Durchlauf des Arrays - Itestat
                        itemstat2 = bag[k]  # Durchlauf des Arrays - Itestat 2
                        embed.add_field(name=f"Slot {slot}",
                                        value=f"Nahrung: {itemname[0]} | HP + {itemstat[1]} {emojilist[1]} | SP + {itemstat2[2]} {emojilist[2]}",
                                        inline=False
                                        )
                        j += 1
                        i += 1
                        k += 1
                        slot += 1

                    embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                    await interaction.message.edit(
                        content=f"Die leckerste Tasche von allen {interaction.user.mention}",
                        embed=embed
                    )
                    await interaction.response.defer()

        if "Schätze" in interaction.data["values"]:
            async with aiosqlite.connect("inventory.db") as db:
                async with db.execute("""SELECT name, gewicht FROM schatz WHERE owner_id = ?""",
                                      (interaction.user.id,)) as cursor:
                    bag = await cursor.fetchall()
                    await cursor.close()

                    embed = discord.Embed(title=f"Schatz-Loot {emojilist[4]}",
                                          color=discord.Color.dark_purple())

                    maxcap = float(100)
                    i = 0  # Durchlauf des Arrays - Itemname
                    slot = 1
                    rows = len(bag)

                    if not bag:
                        embed.add_field(name="404 Schatz not Found",
                                        value="Anscheinend hast du garkeine Schätze in deiner Tasche :cry:",
                                        inline=False)
                        await interaction.message.edit(
                            content=f"Deine Taschen sind leer {interaction.user.mention}",
                            embed=embed
                        )
                        await interaction.response.defer()
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
                                          (interaction.user.id,)) as cursor:
                        gewichttup = await cursor.fetchall()
                        gewicht = itertools.chain(*gewichttup)
                        await cursor.close()

                    embed.set_footer(text=f"Verfübares Gewicht: {abs(maxcap - sum(gewicht))}kg")

                    await interaction.message.edit(
                        content=f"Die Tasche glitzert aber schön {interaction.user.metion}",
                        embed=embed
                    )
                    await interaction.response.defer()

        if "Crafting" in interaction.data["values"]:
            async with aiosqlite.connect("inventory.db") as db:
                async with db.execute("""SELECT name, quality FROM crafting WHERE owner_id = ?""",
                                      (interaction.user.id,)) as cursor:
                    bag = await cursor.fetchall()
                    await cursor.close()

                    embed = discord.Embed(title="Crafting-Items `ICON`",
                                          color=discord.Color.dark_purple())

                    maxcap = 9
                    i = 0  # Durchlauf des Arrays - Itemname
                    slot = 1
                    rows = len(bag)

                    if not bag:
                        embed.add_field(name="404 Item not Found",
                                        value="Anscheinend hast du garkeine Craftingitems in deiner Tasche :cry:",
                                        inline=False
                                        )

                        await interaction.message.edit(
                            content=f"Deine Taschen sind leer {interaction.user.mention}",
                            embed=embed
                        )
                        await interaction.response.defer()
                        return

                    for rows in bag:
                        itemname = bag[i]  # Durchlauf des Arrays - Itemname
                        embed.add_field(name=f"Slot {slot}", value=f"Item: {itemname[0]} | Quality: {itemname[1]} ",
                                        inline=False)
                        i += 1
                        slot += 1

                    embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                    await interaction.message.edit(
                        content=f"Die perfekte Tasche für Basteler {interaction.user.mention}",
                        embed=embed
                    )
                    await interaction.response.defer()

        if "Sonstiges" in interaction.data["values"]:
            async with aiosqlite.connect("inventory.db") as db:
                async with db.execute("""SELECT name FROM rest WHERE owner_id = ?""", (interaction.user.id,)) as cursor:
                    bag = await cursor.fetchall()
                    await cursor.close()

                    embed = discord.Embed(title=f"Sonstige Items {emojilist[6]}",
                                          color=discord.Color.dark_purple())

                    maxcap = 9
                    i = 0  # Durchlauf des Arrays - Itemname
                    slot = 1
                    rows = len(bag)

                    if not bag:
                        embed.add_field(name="404 Item not Found",
                                        value="Anscheinend hast du garkeine Sonstigen Items in deiner Tasche :cry:",
                                        inline=False)
                        await interaction.message.edit(
                            content=f"Deine Taschen sind leer {interaction.user.mention}",
                            embed=embed
                        )
                        await interaction.response.defer()
                        return

                    for rows in bag:
                        itemname = bag[i]  # Durchlauf des Arrays - Itemname
                        embed.add_field(name=f"Slot {slot}", value=f"Item: {itemname[0]} ",
                                        inline=False)
                        i += 1
                        slot += 1

                    embed.set_footer(text=f"Verfübare Slots: {abs(maxcap - i) + 1}")

                    await interaction.message.edit(
                        content=f"Niemand weiß was eigentlich in die Tasche kommt {interaction.user.mention}",
                        embed=embed
                    )
                    await interaction.response.defer()

        if "Close" in interaction.data["values"]:
            select.disabled = True
            await interaction.response.edit_message(content="Tasche geschlossen",
                                                    view=self)



def setup(bot):
    bot.add_cog(Inventar(bot))
