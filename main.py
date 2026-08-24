import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(".",intents=intents)

@bot.event
async def on_ready():
    print("Bot iniciou com sucesso")

@bot.command()
async def Hello(ctx:commands.Context):
    await ctx.reply("Hello, how are you?")

bot.run("")