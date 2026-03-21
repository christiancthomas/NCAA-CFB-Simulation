from player import Player, POSITION_GROUPS, LEGACY_POSITION_MAP as PLAYER_LEGACY_MAP

LEGACY_POSITION_MAP = {
    'Offensive Tackle': ['Left Tackle', 'Right Tackle'],
    'Offensive Guard': ['Left Guard', 'Right Guard'],
    'Linebacker': ['Outside Linebacker', 'Middle Linebacker'],
    'Safety': ['Free Safety', 'Strong Safety'],
}

# Starter requirements for each unit
OFFENSE_STARTERS = {
    'Quarterback': 1,
    'Running Back': 1,
    'Wide Receiver': 3,
    'Tight End': 1,
    'Left Tackle': 1,
    'Left Guard': 1,
    'Center': 1,
    'Right Guard': 1,
    'Right Tackle': 1,
}

DEFENSE_STARTERS = {
    'Edge': 2,
    'Defensive Tackle': 2,
    'Outside Linebacker': 1,
    'Middle Linebacker': 1,
    'Cornerback': 3,
    'Free Safety': 1,
    'Strong Safety': 1,
}

SPECIAL_TEAMS_STARTERS = {
    'Kicker': 1,
    'Punter': 1,
}


class Team:
    def __init__(self, name, nickname=None, city=None, state=None, enrollment=None, conference=None):
        self.name = name
        self.nickname = nickname
        self.city = city
        self.state = state
        self.enrollment = enrollment
        self.conference = conference
        self.players = self.create_players()
        self._depth_chart = None  # Cache for depth chart

    def create_players(self):
        positions = (
            ['Quarterback'] * 3 +
            ['Running Back'] * 4 +
            ['Wide Receiver'] * 8 +
            ['Tight End'] * 4 +
            ['Left Tackle'] * 3 +
            ['Left Guard'] * 3 +
            ['Center'] * 2 +
            ['Right Guard'] * 3 +
            ['Right Tackle'] * 3 +
            ['Edge'] * 6 +
            ['Defensive Tackle'] * 5 +
            ['Outside Linebacker'] * 6 +
            ['Middle Linebacker'] * 4 +
            ['Cornerback'] * 8 +
            ['Free Safety'] * 3 +
            ['Strong Safety'] * 3 +
            ['Kicker'] * 1 +
            ['Punter'] * 1
        )
        players = [Player.generate_random_player(position) for position in positions]
        return players

    def get_players(self, **kwargs):
        matching_players = self.players
        for attr, value in kwargs.items():
            if attr == 'position' and isinstance(value, str) and value in LEGACY_POSITION_MAP:
                # Handle legacy position names by expanding to specific positions
                matching_players = [player for player in matching_players if getattr(player, attr) in LEGACY_POSITION_MAP[value]]
            elif isinstance(value, list):
                matching_players = [player for player in matching_players if getattr(player, attr) in value]
            else:
                matching_players = [player for player in matching_players if getattr(player, attr) == value]
        return matching_players

    def display_team(self):
        print(f"{self.name} {self.nickname}")
        for player in self.players:
            print(f"Player: {player.first_name}, {player.last_name}, Number: {player.number}, Position: {player.position}, Rating: {player.rating}")

    @property
    def depth_chart(self):
        """Returns a dict organizing players by position, sorted by rating (highest first)."""
        if self._depth_chart is None:
            self._depth_chart = self._build_depth_chart()
        return self._depth_chart

    def _build_depth_chart(self):
        """Build depth chart organized by position, sorted by rating descending."""
        chart = {}
        for player in self.players:
            position = player.position
            if position not in chart:
                chart[position] = []
            chart[position].append(player)

        # Sort each position by rating (highest first)
        for position in chart:
            chart[position].sort(key=lambda p: p.rating, reverse=True)

        return chart

    def invalidate_depth_chart(self):
        """Call this when roster changes to rebuild depth chart."""
        self._depth_chart = None

    def get_starters(self):
        """Returns a dict of starting players for each position group.

        Returns:
            dict: Contains 'offense', 'defense', and 'special_teams' keys,
                  each mapping positions to their starting player(s).

        Offense (11 players): 1 QB, 1 RB, 3 WR, 1 TE, 1 LT, 1 LG, 1 C, 1 RG, 1 RT
        Defense (11 players - 4-2-5 Nickel): 2 Edge, 2 DT, 1 OLB, 1 MLB, 3 CB, 1 FS, 1 SS
        Special Teams: 1 K, 1 P
        """
        starters = {
            'offense': {},
            'defense': {},
            'special_teams': {},
        }

        # Offense starters
        for position, count in OFFENSE_STARTERS.items():
            players_at_pos = self.depth_chart.get(position, [])
            starters['offense'][position] = players_at_pos[:count]

        # Defense starters
        for position, count in DEFENSE_STARTERS.items():
            players_at_pos = self.depth_chart.get(position, [])
            starters['defense'][position] = players_at_pos[:count]

        # Special teams starters
        for position, count in SPECIAL_TEAMS_STARTERS.items():
            players_at_pos = self.depth_chart.get(position, [])
            starters['special_teams'][position] = players_at_pos[:count]

        return starters

    def get_starter(self, position):
        """Returns the #1 player (highest rated) at a given position.

        Args:
            position (str): The position to get the starter for.

        Returns:
            Player: The highest-rated player at that position, or None if no players.
        """
        players_at_pos = self.depth_chart.get(position, [])
        return players_at_pos[0] if players_at_pos else None

    def get_backup(self, position, depth=2):
        """Returns the nth player at a position.

        Args:
            position (str): The position to get the backup for.
            depth (int): The depth to retrieve (1=starter, 2=first backup, etc.). Default is 2.

        Returns:
            Player: The player at the specified depth, or None if not enough players.
        """
        players_at_pos = self.depth_chart.get(position, [])
        index = depth - 1  # Convert to 0-indexed
        return players_at_pos[index] if index < len(players_at_pos) else None
