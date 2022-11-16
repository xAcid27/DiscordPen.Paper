import discord, os
from dotenv import load_dotenv
from discord.ext import commands
from discord.commands import slash_command, Option


intents = discord.Intents.default()
intents.members = True
intents.messages = True

activity = discord.Activity(prefix="!" , type=discord.ActivityType.playing, name="Stift und Papier")

bot = discord.Bot(
    intents=intents,
    debug_guilds=None,
    activity=activity
)


@bot.event
async def on_ready():
    print(f"{bot.user} Bot ist online!")


# Pingtest
@bot.slash_command(description="Ping Pong!")
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.respond("Ping ausgeführt", ephemeral=True)


# userInfo function
@bot.slash_command(description="DevUserInfo", name="userinfo")
async def info(ctx, member: Option(discord.Member, "Wähle einen Benutzer", required=False)):

    if member is None:
        member = ctx.author

    embed = discord.Embed(title="Dev Userinfo",
                          description=f"User: {member}",
                          color=discord.Color.dark_purple())

    time = discord.utils.format_dt(member.created_at, "f")

    embed.set_thumbnail(
        url=member.display_avatar,
        )

    embed.add_field(name="ID", value=member.id,)
    embed.add_field(name="Rolle", value=member.top_role)
    embed.add_field(name="Creation", value=time, inline=False)
    embed.set_footer(text="MMODevInfo")

    await ctx.respond(embed=embed)


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

load_dotenv()
bot.run(os.getenv("TOKEN"))
