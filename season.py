import random
from game import Game

class Season:
    def __init__(self, teams):
        self.teams = teams
        self.schedule = []
        self.standings = {team.name: {'wins': 0, 'losses': 0, 'ties': 0} for team in teams}

    def generate_schedule(self):
        # Simple round-robin schedule for demonstration purposes
        # Modify this to account for specific conference rules
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                self.schedule.append((self.teams[i], self.teams[j]))
        random.shuffle(self.schedule)

    def play_game(self, home_team, away_team):
        game = Game(home_team.name, away_team.name)
        game.start_game()
        if game.winner:
            self.standings[game.winner.name]['wins'] += 1
            self.standings[game.loser.name]['losses'] += 1
        else:
            self.standings[home_team.name]['ties'] += 1
            self.standings[away_team.name]['ties'] += 1

    def play_season(self):
        self.generate_schedule()
        for home_team, away_team in self.schedule:
            self.play_game(home_team, away_team)

    def get_top_teams(self):
        sorted_teams = sorted(self.teams, key=lambda team: (self.standings[team.name]['wins'], -self.standings[team.name]['losses']), reverse=True)
        return sorted_teams[:8]

    def display_standings(self):
        for team, record in self.standings.items():
            print(f"{team}: {record['wins']}W-{record['losses']}L-{record['ties']}T")
