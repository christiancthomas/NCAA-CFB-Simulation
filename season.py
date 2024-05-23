import random
from game import Game
from collections import defaultdict

class Season:
    def __init__(self, teams):
        self.year = 2024
        self.week = 1
        self.teams = teams
        self.schedule = defaultdict(list)
        self.standings = {team.name: {'wins': 0, 'losses': 0, 'ties': 0} for team in teams}

    def generate_schedule(self):
        conference_teams = defaultdict(list)
        for team in self.teams:
            conference_teams[team.conference].append(team)

        # Each team plays 8-9 in-conference games
        for conference, teams in conference_teams.items():
            num_teams = len(teams)
            for team in teams:
                # Ensure we do not try to select more in-conference games than available teams
                in_conference_games = min(random.randint(8, 9), num_teams - 1)
                selected_teams = random.sample([t for t in teams if t != team], in_conference_games)
                for opponent in selected_teams:
                    self.schedule[team].append(opponent)
                    self.schedule[opponent].append(team)

        # Add out-of-conference games to each team until they have 12-14 games
        all_teams = list(self.teams)
        for team in self.teams:
            total_games = len(self.schedule[team])
            additional_games = random.randint(12, 14) - total_games
            if additional_games > 0:
                possible_opponents = [t for t in all_teams if t != team and t not in self.schedule[team]]
                selected_teams = random.sample(possible_opponents, min(additional_games, len(possible_opponents)))
                for opponent in selected_teams:
                    self.schedule[team].append(opponent)
                    self.schedule[opponent].append(team)

        # Spread games across 16 weeks
        week_schedule = defaultdict(list)
        for week in range(1, 17):
            for team, opponents in self.schedule.items():
                if len(opponents) > 0:
                    opponent = opponents.pop(0)
                    week_schedule[week].append((team, opponent))
                    self.schedule[opponent].remove(team)

        self.schedule = week_schedule
        print(self.schedule)

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
        for week, games in self.schedule.items():
            print(f"Week {week}:")
            for home_team, away_team in games:
                self.play_game(home_team, away_team)
                print(f"{home_team.name} vs {away_team.name}")

    def get_top_teams(self):
        sorted_teams = sorted(self.teams, key=lambda team: (self.standings[team.name]['wins'], -self.standings[team.name]['losses']), reverse=True)
        return sorted_teams[:8]

    def display_standings(self):
        for team, record in self.standings.items():
            print(f"{team}: {record['wins']}W-{record['losses']}L-{record['ties']}T")
