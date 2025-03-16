import test_setup
import unittest
import random
import numpy as np
from team import Team
from play import create_play, RunPlay, PassPlay, Play

class TestPlay(unittest.TestCase):
    """Test cases for the Play class hierarchy"""

    def setUp(self):
        """Set up test fixtures before each test"""
        random.seed(42)  # Set seed for reproducibility
        np.random.seed(42)
        self.offense = Team("Offense University")
        self.defense = Team("Defense Tech")

    def test_play_abstract_class(self):
        """Test that the base Play class cannot be instantiated directly"""
        # Creating a Play object should raise NotImplementedError when execute() is called
        play = Play(self.offense, self.defense)
        with self.assertRaises(NotImplementedError):
            play.execute()

    def test_play_factory_run(self):
        """Test that the factory function creates run plays correctly"""
        run_play = create_play('run', self.offense, self.defense)
        self.assertIsInstance(run_play, RunPlay)

    def test_play_factory_pass(self):
        """Test that the factory function creates pass plays correctly"""
        pass_play = create_play('pass', self.offense, self.defense)
        self.assertIsInstance(pass_play, PassPlay)

    def test_play_factory_invalid(self):
        """Test that the factory function raises an error for invalid play types"""
        with self.assertRaises(ValueError):
            create_play('invalid_type', self.offense, self.defense)

    def test_run_play_execution(self):
        """Test that a run play executes and returns yards gained"""
        run_play = create_play('run', self.offense, self.defense)
        yards = run_play.execute()

        # We can't predict exact yards due to randomness, but we can check it's a number
        self.assertIsInstance(yards, (int, float))

        # Check that the phase was set during execution
        self.assertIsNotNone(run_play.phase)

    def test_pass_play_execution(self):
        """Test that a pass play executes and returns yards gained"""
        pass_play = create_play('pass', self.offense, self.defense)
        yards = pass_play.execute()

        # We can't predict exact yards due to randomness, but we can check it's a number
        self.assertIsInstance(yards, (int, float))

        # Check pass-specific attributes
        if pass_play.turnover:
            # If turnover, yards should be negative or zero
            self.assertLessEqual(yards, 0)
        elif yards == 0:
            # If incomplete, yards_gained attribute would be None but function returns 0
            self.assertIsNone(pass_play.yards_gained)
        else:
            # If complete with positive yards, yards_gained should be positive
            self.assertGreater(yards, 0)
            self.assertEqual(yards, pass_play.yards_gained)

    def test_pick_from_bell_curve(self):
        """Test that _pick_from_bell_curve returns values in the specified range"""
        play = RunPlay(self.offense, self.defense)

        # Test with different ranges
        for _ in range(100):  # Test multiple times
            min_val, max_val = -5, 10
            result = play._pick_from_bell_curve(min_val, max_val)
            self.assertGreaterEqual(result, min_val)
            self.assertLessEqual(result, max_val)
            self.assertIsInstance(result, int)

    def test_yards_gained_helper(self):
        """Test that _yards_gained_helper returns appropriate values for each phase"""
        play = RunPlay(self.offense, self.defense)

        # Test backfield phase
        backfield_yards = play._yards_gained_helper('backfield')
        self.assertGreaterEqual(backfield_yards, -4)
        self.assertLessEqual(backfield_yards, 4)

        # Test second level phase
        second_level_yards = play._yards_gained_helper('second level')
        self.assertGreaterEqual(second_level_yards, 2)
        self.assertLessEqual(second_level_yards, 7)

        # Test open field phase
        open_field_yards = play._yards_gained_helper('open field')
        self.assertGreaterEqual(open_field_yards, 8)
        self.assertLessEqual(open_field_yards, 99)

        # Test invalid phase
        with self.assertRaises(ValueError):
            play._yards_gained_helper('invalid phase')


if __name__ == '__main__':
    unittest.main()
