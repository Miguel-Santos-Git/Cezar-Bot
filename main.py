#librarys
import discord
from discord.ext import commands
import sqlite3
import json
import time
import random
from enemy import Enemy 
from views.battle_views import start_battle_view as Battle_view

#defalth vars
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".",intents=intents)

connection = sqlite3.connect("usersinfo.db")

with open("configs.json","r") as file:
    token = json.load(file)["token"]

with open("mobs_info.json","r") as file:
    all_monsters = json.load(file)

# starters:
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS main_table (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                money INTEGER NOT NULL
                )""")


# functions
def find_by_character_name(name):
    try:
        cursor.execute("SELECT * FROM main_table WHERE name = ?",(name,))
        return cursor.fetchone()
    except:
        return None

def find_by_user_id(user_id):
    try:
        cursor.execute("SELECT * FROM main_table WHERE user_id = ?",(user_id,))
        return cursor.fetchone()
    except:
        return None

def valid_level_monsters(level):
    valid_monsters = {}
    for id,value in all_monsters.items():
        if value["levelmin"]<=level and value["levelmax"]>level:
            valid_monsters[id] = value
    return valid_monsters

def select_by_weight(objs):
    values = list(objs.keys())

    weights = [
    objs[value]["weight"]
    for value in values
    ]

    selected = random.choices(
    values,
    weights=weights,
    k=1
    )[0]
    return selected

# bot commands
@bot.event
async def on_ready():
    sings = await bot.tree.sync()
    print(f"{len(sings)} comands sync.")
    print("Bot start with sucess.")

@bot.tree.command(description = "Create user info",)
async def create_character(interaction: discord.Interaction, name:str):
    already_char = find_by_user_id(interaction.user.id)
    if already_char is not None:
        await interaction.response.send_message(f"You already have a character.")
        return
    
    infos = find_by_character_name(name)
    if infos:
        await interaction.response.send_message(f"This name already in use.")
        return
    
    cursor.execute("""
    INSERT INTO main_table (user_id, name, level, money)
    VALUES (?, ?, 1, 0)""",
    (interaction.user.id, name))

    connection.commit()
    await interaction.response.send_message(f"Your RP character is create with sucess.")

@bot.tree.command(description = "Get your character info")
async def get_infos(interaction: discord.Interaction):
    infos = find_by_user_id(interaction.user.id)
    if not infos:
        await interaction.response.send_message(f"You dont have a character. Use '/create_character character_name'")
        return

    _, _, name, level, money, _, _ = infos

    await interaction.response.send_message(f"""
    __Your infos:__
    - Character Name: {name}
    - Level: {level}
    - Money: {money}
    """) 

@bot.tree.command(description = "Start a hunt, for increase your money and xp")
async def hunt(interaction: discord.Interaction):
    infos = find_by_user_id(interaction.user.id)
    if not infos:
        await interaction.response.send_message(f"You dont have a character. Use '/create_character character_name'")
        return
    
    _, _, _, level, _, _, _ = infos

    in_level_monsters = valid_level_monsters(level)
    select_monster = select_by_weight(in_level_monsters)

    monster = Enemy(all_monsters[select_monster])
    infos = monster.get_infos()

    view = Battle_view(monster,interaction.user.id)

    await interaction.response.send_message(f""" 
    __Select enemy:__
- Name: {infos["name"]}
- Base damage: {infos["base_damage"]}
- Max life: {infos["maxlife"]}
- Level: {infos["level"]}   
    """, view=view)


connection.commit()

bot.run(token)