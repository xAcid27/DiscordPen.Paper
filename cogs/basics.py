import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Base(commands.Cog):  # Baseclass quasi Gerüst
    def __init__(self, bot):
        self.bot = bot

    # Listen for Welcome
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title=":game_die: | Ein kritischen Erfolg auf deine Anwesenheit",
                              description=f"Herzlich Wilkommen {member.mention}. \n Habe Spaß und möge das "
                                          f"Würfelglück mit dir sein.",
                              color=discord.Color.og_blurple()
                              )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/987385408797175878/1035358361090281542/ezgif-1-d50c6eb6d8.gif")

        channel = await self.bot.fetch_channel(1031620733689921546)  # ChanelID zum Empfangschannel
        await channel.send(embed=embed)

    # clearChannel
    @slash_command(description="Feg doch einfachmal den Channel durch")
    async def clear(self,
                    ctx,
                    amount: Option(int, "Anzahl der der Nachrichten", required=False)):
        if amount is None:
            await ctx.channel.purge(limit=1000)
            await ctx.respond("Clear :broom:")
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.respond("Clear :broom:")


def setup(bot):
    bot.add_cog(Base(bot))
