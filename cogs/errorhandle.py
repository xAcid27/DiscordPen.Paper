import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class errorhandle(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

# Errorhandle
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        await ctx.respond(f"Es ist ein Fehler aufgetreten!: ```{error}```")  #Ausgabe im Discordchat
        raise error  #Ausgabe in der Konsole


def setup(bot):
    bot.add_cog(errorhandle(bot))