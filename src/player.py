import random

POSITION_GROUPS = {
    'QB': ['Quarterback'],
    'RB': ['Running Back'],
    'WR': ['Wide Receiver'],
    'TE': ['Tight End'],
    'OL': ['Left Tackle', 'Left Guard', 'Center', 'Right Guard', 'Right Tackle'],
    'DL': ['Defensive Tackle', 'Edge'],
    'LB': ['Outside Linebacker', 'Middle Linebacker'],
    'DB': ['Cornerback', 'Free Safety', 'Strong Safety'],
    'K': ['Kicker'],
    'P': ['Punter'],
}

POSITION_TO_GROUP = {pos: group for group, positions in POSITION_GROUPS.items() for pos in positions}

# Maps specific positions to their legacy/general position names (for jersey number generation)
LEGACY_POSITION_MAP = {
    'Quarterback': 'Quarterback',
    'Running Back': 'Running Back',
    'Wide Receiver': 'Wide Receiver',
    'Tight End': 'Tight End',
    'Left Tackle': 'Offensive Tackle',
    'Left Guard': 'Offensive Guard',
    'Center': 'Center',
    'Right Guard': 'Offensive Guard',
    'Right Tackle': 'Offensive Tackle',
    'Edge': 'Edge',
    'Defensive Tackle': 'Defensive Tackle',
    'Outside Linebacker': 'Linebacker',
    'Middle Linebacker': 'Linebacker',
    'Cornerback': 'Cornerback',
    'Free Safety': 'Safety',
    'Strong Safety': 'Safety',
    'Kicker': 'Kicker',
    'Punter': 'Punter',
}


class Player:
    def __init__(self, first_name, last_name, position, rating, number,
                 side=None, class_desc='Freshman', years_played=0, redshirt=False
                 ):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.rating = rating
        self.number = number
        self.side = side
        self.class_desc = class_desc
        self.years_played = years_played
        self.redshirt = redshirt

    def _define_side(self, position):
        if position in ['Quarterback', 'Running Back', 'Wide Receiver', 'Tight End', 'Left Tackle', 'Left Guard', 'Center', 'Right Guard', 'Right Tackle', 'Kicker', 'Punter']:
            self.side = 'offense'
        else:
            self.side = 'defense'

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
            case 'Left Tackle' | 'Right Tackle':
                while number in o_nums:
                    number = random.randrange(50, 79)
                o_nums.append(number)
            case 'Left Guard' | 'Right Guard':
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
            case 'Outside Linebacker' | 'Middle Linebacker':
                while number in d_nums:
                    number = random.choice([random.randrange(0,19), random.randint(30, 59)])
                d_nums.append(number)
            case 'Cornerback':
                while number in d_nums:
                    number = random.randrange(0,49)
                d_nums.append(number)
            case 'Free Safety' | 'Strong Safety':
                while number in d_nums:
                    number = random.randrange(0,49)
                d_nums.append(number)
            case 'Kicker':
                while number in o_nums:
                    number = random.choice([random.randint(0, 19), random.randint(90, 99)])
                o_nums.append(number)
            case 'Punter':
                while number in o_nums:
                    number = random.choice([random.randint(0, 19), random.randint(90, 99)])
                o_nums.append(number)

        # defining side of ball
        if position in ['Quarterback', 'Running Back', 'Wide Receiver', 'Tight End', 'Left Tackle', 'Left Guard', 'Center', 'Right Guard', 'Right Tackle', 'Kicker', 'Punter']:
            side = 'offense'
        elif position in ['Kicker', 'Punter']:
            side = 'special teams'
        else:
            side = 'defense'

        return Player(
            first_name=f"{position}",
            last_name=f"{number}",
            position=position,
            rating=random.randint(50, 99),
            number=number,
            side=side
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

