from player import Player

class Team:
    def __init__(self, name, nickname=None, city=None, state=None, enrollment=None, conference=None):
        self.name = name
        self.nickname = nickname
        self.city = city
        self.state = state
        self.enrollment = enrollment
        self.conference = conference
        self.players = self.create_players()

    def create_players(self):
        positions = ['Quarterback', 'Running Back', 'Wide Receiver', 'Wide Receiver', 'Wide Receiver', 'Offensive Tackle', 'Offensive Tackle', 'Offensive Guard',
                     'Offensive Guard', 'Center', 'Tight End', 'Edge', 'Edge', 'Defensive Tackle', 'Defensive Tackle', 'Linebacker', 'Cornerback', 'Cornerback',
                     'Cornerback', 'Safety', 'Safety']
        players = [Player.generate_random_player(position) for position in positions]
        return players
    
    def get_players(self, **kwargs):
        matching_players = self.players
        for attr, value in kwargs.items():
            if isinstance(value, list):
                matching_players = [player for player in matching_players if getattr(player, attr) in value]
            else:
                matching_players = [player for player in matching_players if getattr(player, attr) == value]
        return matching_players if len(matching_players) > 1 else (matching_players[0] if matching_players else None)

    def display_team(self):
        print(f"{self.name} {self.nickname}")
        for player in self.players:
            print(f"Player: {player.name}, Position: {player.position}, Skill Level: {player.skill_level}")
