import random

class Player:
    def __init__(self, name, position, skill_level, number):
        self.name = name
        self.position = position
        self.skill_level = skill_level
        self.number = number

    # @staticmethod
    def generate_random_player(position):
        o_nums = [100]
        d_nums = [100]
        number = 100
        # number generation
        match position:
            case 'Quarterback':
                while number in o_nums:
                    number = random.randrange(1, 19)
                o_nums.append(number)
            case 'Running Back':
                while number in o_nums:
                    number = random.randrange(0,49)
                o_nums.append(number)
            case 'Wide Receiver':
                while number in o_nums:
                    number = random.choice([random.randint(0, 19), random.randint(80, 89)])
                o_nums.append(number)
            case 'Tight End':
                while number in o_nums:
                    number = random.choice([random.randint(0, 19), random.randint(80, 89)])
                o_nums.append(number)
            case 'Offensive Tackle':
                while number in o_nums:
                    number = random.randrange(50, 79)
                o_nums.append(number)
            case 'Offensive Guard':
                while number in o_nums:
                    number = random.randrange(50, 79)
                o_nums.append(number)
            case 'Center':
                while number in o_nums:
                    number = random.randrange(50, 79)
                o_nums.append(number)
            case 'Edge':
                while number in d_nums:
                    number = random.randrange(0,99)
                d_nums.append(number)
            case 'Defensive Tackle':
                while number in d_nums:
                    number = random.randrange(0,99)
                d_nums.append(number)
            case 'Linebacker':
                while number in d_nums:
                    number = random.choice([random.randrange(0,19), random.randint(30, 59)])
                d_nums.append(number)
            case 'Cornerback':
                while number in d_nums:
                    number = random.randrange(0,49)
                d_nums.append(number)
            case 'Safety':
                while number in d_nums:
                    number = random.randrange(0,49)
                d_nums.append(number)

        return Player(
            name=f"{position} {number}",
            position=position,
            skill_level=random.randint(50, 99),
            number={number}
        )
    
    def update_player(self, attributes):
        """Handles updating player attributes.
        Usage: pass list of attributes and values
        e.g., position='Quarterback'"""
        for attr, value in attributes.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                raise AttributeError(f"Player has no attribute '{attr}'")