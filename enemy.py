import random

class Enemy:

    def __init__(self,infos):
        self.name = infos["name"]
        self.base_damage = infos["base_damage"]
        self.life = infos["life"]
        self.maxlife = infos["life"]
        self.skills = infos["skills"]
        self.level = random.randint(infos["levelmin"], infos["levelmax"])

    def attack(self):
        select_skill = self.skills[random.randint(0, len(self.skills))]
        return select_skill

    def take_damage(self, damage):
        self.health -= damage

        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def get_infos(self):
        infos = {}
        infos["name"] = self.name
        infos["base_damage"] = self.base_damage
        infos["life"] = self.life
        infos["maxlife"] = self.maxlife
        infos["level"] = self.level
        return infos