from team import Team
from player import Player
from play import Play
import unittest

class TestPlay(unittest.TestCase):
    def test_backfield(self):
        home_team = Team("Texas Tech", "Red Raiders")
        away_team = Team("Texas", "Longhorns")
        home_team.display_team()
        away_team.display_team()
        play = Play(home_team, away_team, 'run')._execute_run
        self.assertTrue(play, 1)
if __name__ == "__main__":
    unittest.main()