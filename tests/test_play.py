import test_setup
import unittest
import random
import numpy as np
from unittest.mock import MagicMock, patch
from team import Team
from play import create_play, RunPlay, PassPlay, Play
from src.stats import GameStats

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


    def test_run_play_fumble(self):
        """Test that a run play can produce a fumble turnover."""
        stats = GameStats("Offense University", "Defense Tech")
        run_play = create_play('run', self.offense, self.defense, stats=stats)

        # Force a fumble by patching _check_fumble to always return True
        original_check = run_play._check_fumble
        def always_fumble(ballcarrier, base_rate=0.02):
            # Simulate what _check_fumble does when fumble occurs
            run_play.turnover = True
            run_play.fumble_forced_by = self.defense.get_players(position='Edge')[0]
            if run_play.stats is not None:
                forcer = self.defense.get_players(position='Edge')[0]
                run_play.stats._get_or_create_stats(forcer, self.defense.name).add_forced_fumble()
                run_play.stats._get_or_create_stats(forcer, self.defense.name).add_fumble_recovery()
            return True
        run_play._check_fumble = always_fumble

        yards = run_play.execute()

        # Should be a turnover
        self.assertTrue(run_play.turnover)

        # Carrier should have a fumble recorded
        carrier_stats = stats.get_player_stats(run_play.carrier)
        self.assertIsNotNone(carrier_stats)
        self.assertEqual(carrier_stats.fumbles, 1)

        # A defender should have a forced fumble
        def_totals = stats.get_team_totals("Defense Tech")
        self.assertGreaterEqual(def_totals['forced_fumbles'], 1)

    def test_pass_play_fumble_after_catch(self):
        """Test that a receiver can fumble after catching a pass."""
        stats = GameStats("Offense University", "Defense Tech")
        pass_play = create_play('pass', self.offense, self.defense, stats=stats)

        # We need to force a completion then a fumble.
        # Patch _determine_pass_completion to always complete, then _check_fumble to always fumble.
        def fake_completion(self_play=pass_play):
            self_play.target = self_play.offense.get_players(position=['Wide Receiver', 'Tight End'])[0]
            self_play.yards_gained = 15
            if self_play.stats is not None:
                self_play.stats.record_pass(
                    self_play.passer, self_play.target,
                    completed=True, yards=15,
                    team_name=self_play.offense.name
                )

        def always_fumble(ballcarrier, base_rate=0.02):
            pass_play.turnover = True
            pass_play.fumble_forced_by = self.defense.get_players(position='Edge')[0]
            if pass_play.stats is not None:
                forcer = self.defense.get_players(position='Edge')[0]
                pass_play.stats._get_or_create_stats(forcer, self.defense.name).add_forced_fumble()
                pass_play.stats._get_or_create_stats(forcer, self.defense.name).add_fumble_recovery()
            return True

        pass_play._determine_pass_completion = fake_completion
        pass_play._check_fumble = always_fumble

        yards = pass_play.execute()

        # Should be a turnover
        self.assertTrue(pass_play.turnover)

        # Receiver should have a fumble
        target_stats = stats.get_player_stats(pass_play.target)
        self.assertIsNotNone(target_stats)
        self.assertEqual(target_stats.fumbles, 1)

    def test_check_fumble_respects_probability(self):
        """Test that _check_fumble produces fumbles at a reasonable rate."""
        play = RunPlay(self.offense, self.defense)
        carrier = play.carrier

        # Run 1000 trials with a high base rate to get reliable stats
        fumble_count = 0
        for _ in range(1000):
            play.turnover = False  # reset
            if play._check_fumble(carrier, base_rate=0.50):
                fumble_count += 1
                play.turnover = False  # reset for next iteration

        # With 50% base rate, expect a meaningful number of fumbles
        # (scaled by rating, so won't be exactly 500, but should be well above 0)
        self.assertGreater(fumble_count, 50)
        self.assertLess(fumble_count, 950)

    def test_check_fumble_no_fumble_sets_no_turnover(self):
        """Test that _check_fumble returns False and doesn't set turnover when no fumble."""
        play = RunPlay(self.offense, self.defense)

        # Use base_rate=0 so no fumble ever occurs
        result = play._check_fumble(play.carrier, base_rate=0.0)
        self.assertFalse(result)
        self.assertFalse(play.turnover)


if __name__ == '__main__':
    unittest.main()
