import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".",intents=intents)

with open("token.json","r") as file:
    token = json.load(file)["token"]

@bot.event
async def on_ready():
    sings = await bot.tree.sync()
    print(f"{len(sings)} comandos sincronizados.")
    print("Bot iniciou com sucesso.")

@bot.tree.command(description="Say Hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.display_name}! How are you?")


bot.run(token)