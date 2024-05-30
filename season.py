import random
from collections import defaultdict
from game import Game

class Season:
    def __init__(self, teams):
        self.teams = teams
        self.schedule = defaultdict(list)
        self.results = defaultdict(list)
        self.current_week = 1
        self.standings = {team.name: {'wins': 0, 'losses': 0, 'ties': 0} for team in teams}
        self.generate_schedule()

    def generate_schedule(self):
        conference_teams = defaultdict(list)
        for team in self.teams:
            conference_teams[team.conference].append(team)

        # Each team plays 8-9 in-conference games
        for conference, teams in conference_teams.items():
            num_teams = len(teams)
            for team in teams:
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

    def play_game(self, home_team, away_team):
        game = Game(home_team.name, away_team.name)
        game.start_game()
        if game.winner:
            self.standings[game.winner.name]['wins'] += 1
            self.standings[game.loser.name]['losses'] += 1
        else:
            self.standings[home_team.name]['ties'] += 1
            self.standings[away_team.name]['ties'] += 1
        result = f"{home_team.name} {game.home_score} - {away_team.name} {game.away_score}"
        self.results[self.current_week].append(result)

    def play_week(self):
        if self.current_week in self.schedule:
            games = self.schedule[self.current_week]
            for home_team, away_team in games:
                self.play_game(home_team, away_team)
            self.current_week += 1

    def get_schedule_for_week(self, week):
        if week in self.schedule:
            return [(home_team.name, away_team.name) for home_team, away_team in self.schedule[week]]
        return []

    def get_results(self):
        return self.results[self.current_week - 1] if self.current_week - 1 in self.results else []

    def display_standings(self):
        for team, record in self.standings.items():
            print(f"{team}: {record['wins']}W-{record['losses']}L-{record['ties']}T")

    def get_top_teams(self, top_n=8):
        sorted_teams = sorted(self.standings.items(), key=lambda item: (item[1]['wins'], -item[1]['losses']), reverse=True)
        return [team for team, record in sorted_teams[:top_n]]
