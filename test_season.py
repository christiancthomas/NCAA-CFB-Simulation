import unittest
import random
from player import Player
from team import Team
from game import Game
from season import Season
from team_loader import load_teams_from_json

teams = load_teams_from_json('cfb.json')

class TestSeason(unittest.TestCase):
    def test_conference_schedule(self):
        season = Season(teams)
        self.assertEqual(len(season.matchups), 0)
        season._generate_in_conference_games()
        for matchup in season.matchups:
            print(matchup)
        for matchup in season.schedule:
            print(matchup.name)
        print(season.schedule)


if __name__ == "__main__":
    unittest.main()