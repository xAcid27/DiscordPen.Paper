import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.pages import Page , Paginator


class HelpPage(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self , bot):
        self.bot = bot

    @slash_command(description="Alle Befehle mit Beschreibung für die Spieler an")
    async def spieler_help(self , ctx):
        spielerhelp1 = discord.Embed(title="Spielerhilfe" , color=discord.Color.dark_purple())

        discord.Embed.add_field(spielerhelp1 ,
                                name="/waffen_geben" ,
                                value="Gib einem Spieler etwas zum Verteidigen. Nicht das er noch stirbt")
        discord.Embed.add_field(spielerhelp1 ,
                                name="/medizin_geben" ,
                                value="Gib einem Spieler was zum Gesund werden oder zum Vergiften.")

        spielerhelp2 = discord.Embed(title="Spielerhilfe" , color=discord.Color.dark_purple())
        discord.Embed.add_field(spielerhelp2 ,
                                name="/nahrung_geben" ,
                                value="Lasse deine Mitspieler nicht verhungern und gib Ihnen was ab.")
        discord.Embed.add_field(spielerhelp2 ,
                                name="/schatz_geben" ,
                                value="Lass deine Mitspieler ein wenig an deinem Reichtum teilnehmen")

        spielerhelp3 = discord.Embed(title="Spielerhilfe" , color=discord.Color.dark_purple())
        discord.Embed.add_field(spielerhelp3 ,
                                name="/crafting_geben" ,
                                value="Teile deine Craftingsachen mit einem Mitspieler")
        discord.Embed.add_field(spielerhelp3 ,
                                name="/sonstiges_geben" ,
                                value="Wir wissen alle nicht was in dieser Tasche landet, aber du kannst einem Spieler was davon abgeben.")

        pages = [
            Page(embeds=[spielerhelp1]) ,
            Page(embeds=[spielerhelp2]) ,
            Page(embeds=[spielerhelp3])
        ]

        paginator = Paginator(pages=pages)

        await paginator.respond(ctx.interaction , ephemeral=True)

    @slash_command(description="Alle Befehle mit Beschreibung für den Gamemaster")
    async def gm_help(self , ctx):
        gmhelp1 = discord.Embed(title="Game Master Help" , color=discord.Color.dark_purple())
        discord.Embed.add_field(gmhelp1 , name="/add_waffen" , value="Füge eine Waffe dem Spielerinventar hinzu")
        discord.Embed.add_field(gmhelp1 , name="/lose_waffen" , value="Nehme eine Waffe aus dem Spielerinventar")

        gmhelp2 = discord.Embed(title="Game Master Help 2" , color=discord.Color.dark_purple())
        discord.Embed.add_field(gmhelp2 , name="/add_medizin" ,
                                value="Füge eine Medizin / Gift dem Spielerinventar hinzu")
        discord.Embed.add_field(gmhelp2 , name="/lose_medizin" ,
                                value="Nehme eine Medizin / Gift aus dem Spielerinventar")

        gmhelp3 = discord.Embed(title="Game Master Help 3" , color=discord.Color.dark_purple())
        discord.Embed.add_field(gmhelp3 , name="/add_nahrung" ,
                                value="Füge ein Nahrungsmittel dem Spielerinventar hinzu")
        discord.Embed.add_field(gmhelp3 , name="/lose_nahrung" ,
                                value="Nehme eine Nahrungsmittel aus dem Spielerinventar")

        gmhelp4 = discord.Embed(title="Game Master Help 4" , color=discord.Color.dark_purple())
        discord.Embed.add_field(gmhelp4 , name="/add_schatz" , value="Füge eine ein Schatz dem Spielerinventar hinzu")
        discord.Embed.add_field(gmhelp4 , name="/lose_schatz" ,
                                value="Nehme ein Schatz aus dem Spielerinventar, auch wenn es den Befehl garnicht gibt xD")

        gmhelp5 = discord.Embed(title="Game Master Help 5" , color=discord.Color.dark_purple())
        discord.Embed.add_field(gmhelp5 , name="/add_crafting" ,
                                value="Füge eine ein Crafting Utensil dem Spielerinventar hinzu")
        discord.Embed.add_field(gmhelp5 , name="/lose_crafting" ,
                                value="Nehme ein Crafting Utensil aus dem Spielerinventar")

        gmhelp6 = discord.Embed(title="Game Master Help 6" , color=discord.Color.dark_purple())
        discord.Embed.add_field(gmhelp6 , name="/add_rest" , value="Füge was auch immer dem Spielerinventar hinzu")
        discord.Embed.add_field(gmhelp6 , name="/lose_rest" , value="Nehme was auch immer aus dem Spielerinventar")

        pages = [
            Page(embeds=[gmhelp1]) ,
            Page(embeds=[gmhelp2]) ,
            Page(embeds=[gmhelp3]) ,
            Page(embeds=[gmhelp4]) ,
            Page(embeds=[gmhelp5]) ,
            Page(embeds=[gmhelp6])
        ]

        paginator = Paginator(pages=pages)
        await paginator.respond(ctx.interaction , ephemeral=True)


def setup(bot):
    bot.add_cog(HelpPage(bot))
