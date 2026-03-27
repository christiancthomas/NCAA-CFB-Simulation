import random
from collections import defaultdict
from game import Game
from playoffs import Playoffs
from stats import SeasonStats

class Season:
    def __init__(self, teams):
        self.teams = teams
        self.schedule = defaultdict(list)
        self.results = defaultdict(list)
        self.current_week = 1
        self.standings = {team.name: {'wins': 0, 'losses': 0, 'ties': 0} for team in teams}
        self.matchups = set()
        self.game_stats = {}
        self.season_stats = SeasonStats()
        self.champion = None
        self.playoff_results = []
        self.generate_schedule()

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
                in_conference_games = min(random.randint(8, 9), num_teams - 1)
                selected_teams = random.sample([t for t in teams if t != team], in_conference_games)
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
        """Assigns generated games to specific weeks in the season."""
        # Convert schedule dict to list of unique matchups
        all_matchups = []
        seen = set()
        for team, opponents in self.schedule.items():
            for opponent in opponents:
                key = tuple(sorted([team.name, opponent.name]))
                if key not in seen:
                    seen.add(key)
                    all_matchups.append((team, opponent))

        # Clear and rebuild schedule by week
        self.schedule = defaultdict(list)

        # Assign matchups to weeks, ensuring no team plays twice per week
        week = 1
        while all_matchups and week <= 16:
            teams_this_week = set()
            week_games = []
            remaining = []

            for home, away in all_matchups:
                if home.name not in teams_this_week and away.name not in teams_this_week:
                    week_games.append((home, away))
                    teams_this_week.add(home.name)
                    teams_this_week.add(away.name)
                else:
                    remaining.append((home, away))

            self.schedule[week] = week_games
            all_matchups = remaining
            week += 1

    def play_game(self, home_team, away_team):
        """
        Simulates a game between two teams and updates the standings.
        """
        game = Game(home_team, away_team)
        game.start_game()
        if game.winner:
            self.standings[game.winner.name]['wins'] += 1
            self.standings[game.loser.name]['losses'] += 1
        else:
            self.standings[home_team.name]['ties'] += 1
            self.standings[away_team.name]['ties'] += 1
        result = f"{home_team.name} {game.score.home_score} - {away_team.name} {game.score.away_score}"
        self.results[self.current_week].append(result)
        stats = game.get_stats()
        stats.home_score = game.score.home_score
        stats.away_score = game.score.away_score
        self.game_stats.setdefault(self.current_week, []).append(stats)
        self.season_stats.add_game(stats)

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
        """
        Prints the current standings of all teams.
        """
        for team, record in self.standings.items():
            print(f"{team}: {record['wins']}W-{record['losses']}L-{record['ties']}T")

    def get_top_teams(self, top_n=8):
        sorted_teams = sorted(self.standings.items(), key=lambda item: (item[1]['wins'], -item[1]['losses']), reverse=True)
        return [team for team, record in sorted_teams[:top_n]]

    def is_regular_season_complete(self):
        """Returns True if current_week is past the last week with scheduled games."""
        if not self.schedule:
            return True
        last_week_with_games = max(week for week in self.schedule if self.schedule[week])
        return self.current_week > last_week_with_games

    def get_standings_sorted(self):
        """Returns list of (team_name, record) sorted by wins (desc) then losses (asc)."""
        sorted_standings = sorted(
            self.standings.items(),
            key=lambda item: (item[1]['wins'], -item[1]['losses']),
            reverse=True
        )
        return [(team, record) for team, record in sorted_standings]

    def run_playoffs(self):
        """Run the 8-team playoff after regular season."""
        if not self.is_regular_season_complete():
            raise ValueError("Regular season not complete")

        # Get top 8 teams
        top_teams = self.get_top_teams(8)

        # Need actual Team objects, not just names
        team_objects = [t for t in self.teams if t.name in top_teams]
        # Sort to match standings order
        team_objects.sort(key=lambda t: top_teams.index(t.name))

        playoffs = Playoffs(team_objects)
        champion = playoffs.play_playoffs()
        self.champion = champion
        return champion

    def get_game_stats_for_week(self, week):
        """Returns list of GameStats for the given week."""
        return self.game_stats.get(week, [])

    def get_season_leaders(self, stat, top_n=10):
        """Returns top N players for a given stat across the season."""
        return self.season_stats.get_leaders(stat, top_n)

    def simulate_full_season(self):
        """Simulate entire season including playoffs."""
        # Play all regular season weeks
        while not self.is_regular_season_complete():
            self.play_week()

        # Run playoffs
        return self.run_playoffs()
