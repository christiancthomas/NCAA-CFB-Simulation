import random

class Player:
    def __init__(self, name, position, skill_level, number=0):
        self.name = name
        self.position = position
        self.skill_level = skill_level
        self.number = number

    # @staticmethod
    def generate_random_player(position):
        # number generation
        match position:
            case 'Quarterback': 
                number = random.randrange(1, 19)
            case 'Running Back':
                number = random.randrange(0,49)
            case 'Wide Receiver':
                number = random.choice([random.randint(0, 19), random.randint(80, 89)])
            case 'Linebacker':
                number = random.choice([random.randrange(0,19), random.randint(30, 59)])
            case 'Cornerback':
                number = random.randrange(0,49)
        
        return Player(
            name=f"{position} {number}",
            position=position,
            skill_level=random.randint(50, 100),
            number={number}
        )
