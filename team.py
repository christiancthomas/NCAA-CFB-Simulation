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
        positions = ['Quarterback', 'Running Back', 'Wide Receiver', 'Linebacker', 'Cornerback']
        players = [Player.generate_random_player(position) for position in positions]
        return players

    def display_team(self):
        print(f"Team: {self.name} ({self.nickname})")
        for player in self.players:
            print(f"Player: {player.name}, Position: {player.position}, Skill Level: {player.skill_level}")
