import test_setup
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

    def test_run_distribution(self):
        home_team = Team("Texas Tech", "Red Raiders")
        away_team = Team("Texas", "Longhorns")
        home_team.display_team()
        away_team.display_team()

        yards_gained = []
        cycles = 1
        for _ in range(cycles):
            play = Play(home_team, away_team, 'run')
            play._execute_run()
            yards_gained.append(play.yards_gained)
            print(f"Yards Gained: {play.yards_gained}")

        # Display the final yards gained distribution
        print("Yards Gained Distribution:")
        for i in range(min(yards_gained), max(yards_gained) + 1):
            count = yards_gained.count(i)
            print(f"{i} yards: {count} plays, {count/cycles*100}% of distribution")

if __name__ == "__main__":
    unittest.main()