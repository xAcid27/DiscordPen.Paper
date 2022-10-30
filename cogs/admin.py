import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Admin(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Kicke einen User")
    @commands.has_any_role("Admin", "Spieler", "Spielleiter")
    async def kick(self,
                   ctx,
                   member: Option(discord.Member, "Wähle einen User"),
                   reason: Option(str, "Was ist der Grund")):
        await member.kick()
        await ctx.respond(f"{member.mention} wurde gekickt! || Grund: {reason}")


def setup(bot):
    bot.add_cog(Admin(bot))
