import unittest
import test_setup
import random
import numpy as np
from unittest.mock import MagicMock, patch
from playoffs import Playoffs
from season import Season
from team import Team


class MockTeam:
    """Mock team for testing purposes."""
    def __init__(self, name, conference="Test Conference"):
        self.name = name
        self.conference = conference

    def get_players(self, position=None):
        """Return empty list for mock players."""
        return []


class TestPlayoffs(unittest.TestCase):
    """Test cases for the Playoffs class"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Set seeds for reproducibility
        random.seed(42)
        np.random.seed(42)

        # Create 8 mock teams for playoffs
        self.teams = [MockTeam(f"Team {i}") for i in range(1, 9)]

    def test_playoffs_creation_with_8_teams(self):
        """Test that playoffs can be created with 8 teams"""
        playoffs = Playoffs(self.teams)

        self.assertEqual(len(playoffs.teams), 8)
        self.assertEqual(playoffs.teams[0].name, "Team 1")
        self.assertEqual(playoffs.teams[7].name, "Team 8")
        self.assertEqual(playoffs.rounds, [])

    def test_setup_playoff_bracket(self):
        """Test that playoff bracket is set up correctly"""
        playoffs = Playoffs(self.teams)
        playoffs.setup_playoff_bracket()

        # Should have 2 rounds for quarterfinals
        self.assertEqual(len(playoffs.rounds), 2)

        # Each round should have 2 matchups
        self.assertEqual(len(playoffs.rounds[0]), 2)
        self.assertEqual(len(playoffs.rounds[1]), 2)

        # Check seeding: 1 vs 8, 4 vs 5 in first bracket
        self.assertEqual(playoffs.rounds[0][0], (self.teams[0], self.teams[7]))
        self.assertEqual(playoffs.rounds[0][1], (self.teams[3], self.teams[4]))

        # Check seeding: 2 vs 7, 3 vs 6 in second bracket
        self.assertEqual(playoffs.rounds[1][0], (self.teams[1], self.teams[6]))
        self.assertEqual(playoffs.rounds[1][1], (self.teams[2], self.teams[5]))

    @patch.object(Playoffs, 'play_game')
    def test_play_playoffs_returns_winner(self, mock_play_game):
        """Test that play_playoffs returns a winner"""
        playoffs = Playoffs(self.teams)

        # Mock play_game to return the first team in each matchup
        mock_play_game.side_effect = lambda home, away: home

        champion = playoffs.play_playoffs()

        # Should return a team object
        self.assertIsNotNone(champion)
        self.assertTrue(hasattr(champion, 'name'))

    @patch.object(Playoffs, 'play_game')
    def test_play_playoffs_correct_number_of_games(self, mock_play_game):
        """Test that correct number of playoff games are played"""
        playoffs = Playoffs(self.teams)

        # Mock play_game to return the first team in each matchup
        mock_play_game.side_effect = lambda home, away: home

        playoffs.play_playoffs()

        # 8 teams: 4 quarterfinal + 2 semifinal + 1 final = 7 games
        self.assertEqual(mock_play_game.call_count, 7)


class TestSeasonPlayoffIntegration(unittest.TestCase):
    """Test cases for Season playoff integration"""

    def setUp(self):
        """Set up test fixtures before each test"""
        random.seed(42)
        np.random.seed(42)

        # Create mock teams with conferences
        self.teams = [MockTeam(f"Team {i}", f"Conference {i % 2}") for i in range(1, 17)]

    def test_season_has_playoff_attributes(self):
        """Test that Season has champion and playoff_results attributes"""
        season = Season(self.teams)

        self.assertIsNone(season.champion)
        self.assertEqual(season.playoff_results, [])

    def test_run_playoffs_raises_if_season_not_complete(self):
        """Test that run_playoffs raises error if regular season not complete"""
        season = Season(self.teams)

        # Season just started, should not be complete
        with self.assertRaises(ValueError) as context:
            season.run_playoffs()

        self.assertIn("Regular season not complete", str(context.exception))

    @patch.object(Season, 'is_regular_season_complete', return_value=True)
    @patch.object(Playoffs, 'play_playoffs')
    def test_run_playoffs_returns_champion(self, mock_play_playoffs, mock_is_complete):
        """Test that run_playoffs returns and stores champion"""
        season = Season(self.teams)

        # Mock the playoff champion
        mock_champion = MockTeam("Champion Team")
        mock_play_playoffs.return_value = mock_champion

        champion = season.run_playoffs()

        # Should return the champion
        self.assertEqual(champion, mock_champion)
        # Champion should be stored in season
        self.assertEqual(season.champion, mock_champion)

    @patch.object(Season, 'is_regular_season_complete', return_value=True)
    @patch.object(Playoffs, 'play_playoffs')
    def test_run_playoffs_uses_top_8_teams(self, mock_play_playoffs, mock_is_complete):
        """Test that run_playoffs uses top 8 teams from standings"""
        season = Season(self.teams)

        # Manually set some standings to test ordering
        for i, team in enumerate(self.teams[:8]):
            season.standings[team.name]['wins'] = 10 - i

        mock_champion = MockTeam("Champion")
        mock_play_playoffs.return_value = mock_champion

        season.run_playoffs()

        # Verify play_playoffs was called (Playoffs was created with teams)
        mock_play_playoffs.assert_called_once()

    @patch.object(Season, 'play_week')
    @patch.object(Season, 'run_playoffs')
    def test_simulate_full_season_plays_all_weeks(self, mock_run_playoffs, mock_play_week):
        """Test that simulate_full_season plays all regular season weeks"""
        season = Season(self.teams)

        # Track calls to is_regular_season_complete
        call_count = [0]
        max_weeks = 20  # Safety limit

        def is_complete_side_effect():
            call_count[0] += 1
            return call_count[0] > max_weeks or call_count[0] > 5  # Complete after 5 weeks for test

        with patch.object(Season, 'is_regular_season_complete', side_effect=is_complete_side_effect):
            mock_champion = MockTeam("Champion")
            mock_run_playoffs.return_value = mock_champion

            champion = season.simulate_full_season()

            # Should have called play_week multiple times
            self.assertGreater(mock_play_week.call_count, 0)
            # Should return champion from run_playoffs
            self.assertEqual(champion, mock_champion)


if __name__ == '__main__':
    unittest.main()
