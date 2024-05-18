import unittest
import random
from player import Player
from team import Team
from game import Game

class TestPlayer(unittest.TestCase):
    def test_player_creation(self):
        player = Player("John Doe", "Quarterback", 75)
        self.assertEqual(player.name, "John Doe")
        self.assertEqual(player.position, "Quarterback")
        self.assertEqual(player.skill_level, 75)

    def test_generate_random_player(self):
        player = Player.generate_random_player("Running Back")
        self.assertEqual(player.position, "Running Back")
        self.assertTrue(50 <= player.skill_level <= 100)

class TestTeam(unittest.TestCase):
    def test_team_creation(self):
        team = Team("Tigers")
        self.assertEqual(team.name, "Tigers")
        self.assertEqual(len(team.players), 5)  # Assuming 5 positions

    def test_display_team(self):
        team = Team("Lions")
        # We'll just check that this method runs without error
        team.display_team()

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game("Texas Tech", "Baylor")

    def test_game_initialization(self):
        self.assertEqual(self.game.home.name, "Texas Tech")
        self.assertEqual(self.game.away.name, "Baylor")
        self.assertEqual(self.game.ball_pos_raw, 25)
        self.assertEqual(self.game.ball_pos, 25)
        self.assertEqual(self.game.territory, 'home')
        self.assertEqual(self.game.down, 1)
        self.assertEqual(self.game.yards_to_go, 10)

    def test_calc_ball_pos(self):
        self.game.calc_ball_pos(10)
        self.assertEqual(self.game.ball_pos_raw, 35)
        self.assertEqual(self.game.ball_pos, 15)
        self.assertEqual(self.game.territory, 'home')

    def test_calc_ball_pos_away(self):
        self.game.current_offense = self.game.away
        self.game.calc_ball_pos(10)
        self.assertEqual(self.game.ball_pos_raw, 15)
        self.assertEqual(self.game.ball_pos, 35)
        self.assertEqual(self.game.territory, 'home')

    def test_calc_down_first_down(self):
        self.game.calc_down(10)
        self.assertEqual(self.game.down, 1)
        self.assertEqual(self.game.yards_to_go, 10)

    def test_calc_down_turnover(self):
        self.game.down = 4
        self.game.calc_down(5)
        self.assertEqual(self.game.current_offense, self.game.away)
        self.assertEqual(self.game.current_defense, self.game.home)
        self.assertEqual(self.game.down, 1)
        self.assertEqual(self.game.yards_to_go, 10)

    def test_score_home_touchdown(self):
        self.game.ball_pos_raw = 100
        self.game.score()
        self.assertEqual(self.game.home_score, 6)
        self.assertEqual(self.game.down, 'PAT')
        self.assertEqual(self.game.ball_pos_raw, 98)

    def test_score_away_touchdown(self):
        self.game.ball_pos_raw = 0
        self.game.current_offense = self.game.away
        self.game.score()
        self.assertEqual(self.game.away_score, 6)
        self.assertEqual(self.game.down, 'PAT')
        self.assertEqual(self.game.ball_pos_raw, 2)

    def test_simulate_play_run(self):
        initial_position = self.game.ball_pos_raw
        self.game.simulate_play("run")
        self.assertNotEqual(self.game.ball_pos_raw, initial_position)

    def test_simulate_play_pass(self):
        initial_position = self.game.ball_pos_raw
        self.game.simulate_play("pass")
        self.assertNotEqual(self.game.ball_pos_raw, initial_position)

class TestPlayoffOvertime(unittest.TestCase):
    def test_playoff_overtime(self):
        home_team = Team("Home Team", "Home Nickname")
        away_team = Team("Away Team", "Away Nickname")

        # Create a game with playoff set to True
        game = Game(home_team.name, away_team.name, playoff=True)

        # Simulate the end of the fourth quarter with a tied score
        game.home_score = 24
        game.away_score = 24
        game.clock.quarter = 4
        game.clock.minutes = 0
        game.clock.seconds = 0

        # Ensure the game does not end if it's a playoff game and the score is tied
        game.simulate_play(random.choice(['run', 'pass']))  # Try to end the game

        # Check that the game has gone into overtime
        self.assertIsNone(game.winner, "The game should not have a winner yet.")

        # Simulate overtime until a winner is found
        while game.winner is None:
            game.simulate_play(random.choice(['run', 'pass']))

        # Check that the game now has a winner
        self.assertIsNotNone(game.winner, "The game should have a winner after overtime.")

        print(f"The winner is: {game.winner.name}")

if __name__ == "__main__":
    unittest.main()
