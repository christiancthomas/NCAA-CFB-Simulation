import random

class Player:
    def __init__(self, name, position, skill_level):
        self.name = name
        self.position = position
        self.skill_level = skill_level

    @staticmethod
    def generate_random_player(position):
        return Player(
            name=f"{position} {random.randint(1, 99)}",
            position=position,
            skill_level=random.randint(50, 100)
        )
