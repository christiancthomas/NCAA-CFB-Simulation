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
        self.assertEqual(len(season.matchups), 0)
        season._generate_in_conference_games()
        team_count = dict()
        for matchup in season.matchups:
            for team in matchup:
                if team.name in team_count:
                    team_count[team.name] += 1
                else:
                    team_count[team.name] = 1
            print(f'{matchup[0].name} ({matchup[0].conference}) vs. {matchup[1].name} ({matchup[1].conference})')
            self.assertEqual(matchup[0].conference, matchup[1].conference)
        print(team_count)


if __name__ == "__main__":
    unittest.main()