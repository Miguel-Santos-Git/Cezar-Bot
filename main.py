import discord
from discord.ext import commands
import sqlite3
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".",intents=intents)

connection = sqlite3.connect("usersinfo.db")

cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS main_table (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                money INTEGER NOT NULL
                )""")

with open("configs.json","r") as file:
    token = json.load(file)["token"]

def char_name_exist(name):
    cursor.execute("SELECT * FROM main_table WHERE name = ?",(name,))
    return cursor.fetchone() is not None

def already_have_char(username):
    cursor.execute("SELECT * FROM main_table WHERE username = ?",(username,))
    return cursor.fetchone() is not None

@bot.event
async def on_ready():
    sings = await bot.tree.sync()
    print(f"{len(sings)} comandos sincronizados.")
    print("Bot iniciou com sucesso.")

@bot.tree.command(description="Create user info",)
async def create_character(interaction: discord.Interaction, name:str):
    if not name:
        await interaction.response.send_message(f"You don't select a character name.")
        return
    name_exist = char_name_exist(name)
    if name_exist:
        await interaction.response.send_message(f"This name already in use.")
        return
    already_char = already_have_char(interaction.user.name)
    if already_char:
        await interaction.response.send_message(f"You already have a character.")

    cursor.execute("""
    INSERT INTO main_table (username, name, level, money)
    VALUES (?, ?, 1, 0)
                    """,(interaction.user.name, name))

    connection.commit()
    await interaction.response.send_message(f"Your RP character is create with sucess.")

connection.commit()
bot.run(token)