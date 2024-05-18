from player import Player

class Team:
    def __init__(self, name):
        self.name = name
        self.players = self.create_players()

    def create_players(self):
        positions = ['Quarterback', 'Running Back', 'Wide Receiver', 'Linebacker', 'Cornerback']
        players = [Player.generate_random_player(position) for position in positions]
        return players

    def display_team(self):
        print(f"Team: {self.name}")
        for player in self.players:
            print(f"Player: {player.name}, Position: {player.position}, Skill Level: {player.skill_level}")
