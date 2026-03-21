import test_setup
import unittest
import random
from player import Player
from team import Team
from game import Game
from season import Season
import os
from utils.team_loader import load_teams_from_json

# Construct the path to cfb.json relative to the current file
current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, '..', 'utils', 'cfb.json')

teams = load_teams_from_json(json_path)

class TestSeason(unittest.TestCase):
    def test_conference_schedule(self):
        season = Season(teams)
        # matchups is populated by generate_schedule() called in __init__
        self.assertGreater(len(season.matchups), 0)
        # matchups now stores (team_name, opponent_name) tuples as strings
        team_count = dict()
        for matchup in season.matchups:
            for team_name in matchup:
                if team_name in team_count:
                    team_count[team_name] += 1
                else:
                    team_count[team_name] = 1
        print(f"Total matchups: {len(season.matchups)}")
        print(f"Teams with games: {len(team_count)}")
        season.display_standings()
    
    def test_acc_season(self):
        pass


if __name__ == "__main__":
    unittest.main()