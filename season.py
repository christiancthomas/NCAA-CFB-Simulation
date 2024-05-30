import random
from collections import defaultdict
from game import Game

class Season:
    def __init__(self, teams):
        self.year = 2024
        # self.week = 1
        self.teams = teams
        self.schedule = defaultdict(list)
        self.standings = {team.name: {'wins': 0, 'losses': 0, 'ties': 0} for team in teams}
        self.matchups = set()  # Track scheduled matchups

    def generate_schedule(self):
        """
        Generates a schedule for the season, including in-conference and out-of-conference games.
        """
        self._generate_in_conference_games()
        self._generate_out_of_conference_games()
        self._assign_games_to_weeks()

    def _generate_in_conference_games(self):
        """
        Generate in-conference games for each team.
        """
        conference_teams = defaultdict(list)
        for team in self.teams:
            conference_teams[team.conference].append(team)

        for conference, teams in conference_teams.items():
            num_teams = len(teams)
            for team in teams:
                possible_opponents = [t for t in teams if t != team and (team.name, t.name) not in self.matchups and (t.name, team.name) not in self.matchups]
                in_conference_games = min(random.randint(7, 9), len(possible_opponents))
                selected_teams = random.sample(possible_opponents, in_conference_games)
                for opponent in selected_teams:
                    self.schedule[team].append(opponent)
                    self.schedule[opponent].append(team)
                    self.matchups.add((team.name, opponent.name))  # Track the matchup

    def _generate_out_of_conference_games(self):
        """
        Generate out-of-conference games for each team.
        """
        all_teams = list(self.teams)
        for team in self.teams:
            total_games = len(self.schedule[team])
            additional_games = random.randint(12, 14) - total_games
            if additional_games > 0:
                possible_opponents = [t for t in all_teams if t != team and t not in self.schedule[team] and (team.name, t.name) not in self.matchups and (t.name, team.name) not in self.matchups]
                selected_teams = random.sample(possible_opponents, min(additional_games, len(possible_opponents)))
                for opponent in selected_teams:
                    self.schedule[team].append(opponent)
                    self.schedule[opponent].append(team)
                    self.matchups.add((team.name, opponent.name))  # Track the matchup

    def _assign_games_to_weeks(self):
        """
        Assigns generated games to specific weeks in the season.
        """
        week_schedule = defaultdict(list)
        for week in range(1, 17):
            for team, opponents in self.schedule.items():
                if len(opponents) > 0:
                    opponent = opponents.pop(0)
                    week_schedule[week].append((team, opponent))
                    self.schedule[opponent].remove(team)

        self.schedule = week_schedule

    def play_game(self, home_team, away_team):
        """
        Simulates a game between two teams and updates the standings.
        """
        game = Game(home_team.name, away_team.name)
        game.start_game()
        if game.winner:
            self.standings[game.winner.name]['wins'] += 1
            self.standings[game.loser.name]['losses'] += 1
        else:
            self.standings[home_team.name]['ties'] += 1
            self.standings[away_team.name]['ties'] += 1

    def play_season(self):
        """
        Plays all games in the season, week by week.
        """
        self.generate_schedule()
        for week, games in self.schedule.items():
            print(f"Week {week}:")
            for home_team, away_team in games:
                self.play_game(home_team, away_team)
                print(f"{home_team.name} vs {away_team.name}")

    def get_top_teams(self):
        """
        Returns the top 8 teams based on their win-loss records.
        """
        sorted_teams = sorted(self.teams, key=lambda team: (self.standings[team.name]['wins'], -self.standings[team.name]['losses']), reverse=True)
        return sorted_teams[:8]

    def display_standings(self):
        """
        Prints the current standings of all teams.
        """
        for team, record in self.standings.items():
            print(f"{team}: {record['wins']}W-{record['losses']}L-{record['ties']}T")
