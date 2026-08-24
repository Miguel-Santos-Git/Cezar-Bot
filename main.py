import discord
from discord.ext import commands
import sqlite3
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".",intents=intents)

connection = sqlite3.connect("bank.db")

cursor = connection.cursor()
cursor.execute("""CREATE TABLE main_table (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                money INTEGER NOT NULL
                )""")
connection.commit()

with open("configs.json","r") as file:
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