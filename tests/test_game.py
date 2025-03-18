import unittest
import test_setup
import random
import numpy as np
from unittest.mock import MagicMock, patch
from game import Game
from team import Team
from game_clock import GameClock
from game_state import GameState
from score import Score

class TestGame(unittest.TestCase):
    """Test cases for the Game class"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Set seeds for reproducibility
        random.seed(42)
        np.random.seed(42)

        # Create a test game
        self.game = Game("Home Team", "Away Team")

        # Mock player retrieval instead of trying to add players
        # This lets us test without modifying the actual Team class
        self.mock_players()

    def mock_players(self):
        """Set up mock players for testing"""
        # Create a mock player that can be returned by get_players
        def create_mock_player(first_name, position, rating=75):
            player = MagicMock()
            player.first_name = first_name
            player.last_name = "Test"
            player.position = position
            player.rating = rating
            return player

        # Create mock players for different positions
        qb = create_mock_player("QB", "Quarterback")
        rb = create_mock_player("RB", "Running Back")
        wr = create_mock_player("WR", "Wide Receiver")
        te = create_mock_player("TE", "Tight End")
        ot = create_mock_player("OT", "Offensive Tackle")
        og = create_mock_player("OG", "Offensive Guard")
        c = create_mock_player("C", "Center")
        dt = create_mock_player("DT", "Defensive Tackle")
        edge = create_mock_player("Edge", "Edge")
        lb = create_mock_player("LB", "Linebacker")
        cb = create_mock_player("CB", "Cornerback")
        s = create_mock_player("S", "Safety")

        # Mock the get_players method to return our mock players
        def mock_get_players(position=None):
            if position == 'Quarterback':
                return [qb]
            elif position == 'Running Back':
                return [rb]
            elif position == 'Wide Receiver':
                return [wr]
            elif position == 'Tight End':
                return [te]
            elif position == 'Offensive Tackle':
                return [ot]
            elif position == 'Offensive Guard':
                return [og]
            elif position == 'Center':
                return [c]
            elif position == 'Defensive Tackle':
                return [dt]
            elif position == 'Edge':
                return [edge]
            elif position == 'Linebacker':
                return [lb]
            elif position == 'Cornerback':
                return [cb]
            elif position == 'Safety':
                return [s]
            elif position == ['Defensive Tackle', 'Edge']:
                return [dt, edge]
            elif position == ['Wide Receiver', 'Tight End']:
                return [wr, te]
            elif position == ['Linebacker', 'Cornerback', 'Safety']:
                return [lb, cb, s]
            return []

        # Apply the mock to both teams
        self.game.home.get_players = mock_get_players
        self.game.away.get_players = mock_get_players

    def test_game_initialization(self):
        """Test that a Game object is initialized correctly"""
        game = self.game
        print(f'game.score: {game.score.home_score}')

        # Test teams
        self.assertEqual(game.home.name, "Home Team")
        self.assertEqual(game.away.name, "Away Team")

        # Test initial game state
        self.assertEqual(game.state.down, 1)
        self.assertEqual(game.state.yards_to_go, 10)
        self.assertEqual(game.state.ball_pos_raw, 25)
        self.assertEqual(game.state.ball_pos, 25)
        self.assertEqual(game.state.territory, "home")
        self.assertEqual(game.score.home_score, 0)
        self.assertEqual(game.score.away_score, 0)

        # Test initial offense/defense setup
        self.assertEqual(game.current_offense, game.home)
        self.assertEqual(game.current_defense, game.away)

    def test_coin_toss(self):
        """Test that coin toss assigns offense and defense correctly"""
        game = self.game

        # Perform coin toss
        game.coin_toss()

        # Check that receive and defend are set
        self.assertIsNotNone(game.state.receive)
        self.assertIsNotNone(game.state.defend)

        # Check that offense and defense are assigned properly
        self.assertEqual(game.current_offense, game.state.receive)

        # Either home or away team should be on offense
        self.assertTrue(game.current_offense in [game.home, game.away])
        self.assertTrue(game.current_defense in [game.home, game.away])

        # Offense and defense should be different teams
        self.assertNotEqual(game.current_offense, game.current_defense)

    def test_calc_ball_pos(self):
        """Test that ball position is calculated correctly"""
        game = self.game

        # Test with home team on offense
        game.current_offense = game.home
        game.current_defense = game.away

        # Reset ball position
        game.state.ball_pos_raw = 25

        # Advance 10 yards
        game.calc_ball_pos(10)

        # Ball should be at 35 yard line
        self.assertEqual(game.state.ball_pos_raw, 35)
        self.assertEqual(game.state.ball_pos, 35)
        self.assertEqual(game.state.territory, "home")

        # Advance past midfield
        game.calc_ball_pos(20)

        # Ball should be at 55 yard line (in away territory)
        self.assertEqual(game.state.ball_pos_raw, 55)
        self.assertEqual(game.state.ball_pos, 45)  # 45 yards from goal
        self.assertEqual(game.state.territory, "away")

        # Test with away team on offense
        game.current_offense = game.away
        game.current_defense = game.home

        # Reset ball position
        game.state.ball_pos_raw = 75

        # Advance 10 yards
        game.calc_ball_pos(10)

        # Ball should be at 65 yard line (backwards because away team goes other direction)
        self.assertEqual(game.state.ball_pos_raw, 65)
        self.assertEqual(game.state.ball_pos, 35)
        self.assertEqual(game.state.territory, "away")

    def test_calc_down(self):
        """Test that down calculation works correctly"""
        game = self.game

        # Set initial state
        game.state.down = 1
        game.state.yards_to_go = 10

        # Gain 4 yards on first down
        game.calc_down(4)

        # Should be 2nd and 6
        self.assertEqual(game.state.down, 2)
        self.assertEqual(game.state.yards_to_go, 6)

        # Gain 3 more yards
        game.calc_down(3)

        # Should be 3rd and 3
        self.assertEqual(game.state.down, 3)
        self.assertEqual(game.state.yards_to_go, 3)

        # Gain 1 more yard
        game.calc_down(1)

        # Should be 4th and 2
        self.assertEqual(game.state.down, 4)
        self.assertEqual(game.state.yards_to_go, 2)

        # Turn over on downs (gain 1 yard but need 2)
        original_offense = game.current_offense
        original_defense = game.current_defense

        game.calc_down(1)

        # Should be 1st and 10 with possession changed
        self.assertEqual(game.state.down, 1)
        self.assertEqual(game.state.yards_to_go, 10)
        self.assertEqual(game.current_offense, original_defense)
        self.assertEqual(game.current_defense, original_offense)

    def test_turnover(self):
        """Test that turnover switches offense and defense"""
        game = self.game

        # Set initial offense/defense
        original_offense = game.current_offense
        original_defense = game.current_defense

        # Execute turnover
        game.turnover()

        # Teams should be switched
        self.assertEqual(game.current_offense, original_defense)
        self.assertEqual(game.current_defense, original_offense)

    @patch('play.create_play')
    def test_simulate_play(self, mock_create_play):
        """Test the simulate_play method with mocked play"""
        game = self.game

        # Create a mock play
        mock_play = MagicMock()
        mock_play.turnover = False
        mock_play.execute.return_value = 5  # 5 yard gain

        # Make create_play return our mock
        mock_create_play.return_value = mock_play

        # Set initial game state
        game.state.state = 'down'
        game.state.down = 1
        game.state.yards_to_go = 10

        # Simulate a play
        game.simulate_play('run')

        # Verify create_play was called correctly
        mock_create_play.assert_called_once_with('run', game.current_offense, game.current_defense)

        # Verify execute was called
        mock_play.execute.assert_called_once()

    def test_set_ball(self):
        """Test that set_ball properly positions the ball"""
        game = self.game

        # Test kickoff setup
        game.state.state = 'kickoff'
        game.state.opening = True
        game.current_offense = game.home

        game.set_ball()

        self.assertEqual(game.state.ball_pos_raw, 25)
        self.assertEqual(game.state.down, 1)
        self.assertEqual(game.state.yards_to_go, 10)
        self.assertEqual(game.state.state, 'down')
        self.assertFalse(game.state.opening)

        # Test PAT setup for home team
        game.state.state = 'pat'
        game.current_offense = game.home

        game.set_ball()

        self.assertEqual(game.state.ball_pos_raw, 98)
        self.assertEqual(game.state.down, 'PAT')

        # Test halftime setup
        game.state.state = 'halftime'
        game.state.receive = game.home
        game.state.defend = game.away

        game.set_ball()

        self.assertEqual(game.current_offense, game.away)  # Should switch to the defending team
        self.assertEqual(game.state.down, 1)
        self.assertEqual(game.state.state, 'down')


if __name__ == '__main__':
    unittest.main()
