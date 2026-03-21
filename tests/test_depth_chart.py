import test_setup
from src.team import Team, OFFENSE_STARTERS, DEFENSE_STARTERS, SPECIAL_TEAMS_STARTERS
from player import Player
import unittest


class TestDepthChart(unittest.TestCase):
    def setUp(self):
        """Create a fresh team for each test."""
        self.team = Team("Test Tigers")

    def test_depth_chart_is_dict_organized_by_position(self):
        """Depth chart should be a dict with positions as keys."""
        depth_chart = self.team.depth_chart
        self.assertIsInstance(depth_chart, dict)
        # Check that all players are accounted for
        total_players = sum(len(players) for players in depth_chart.values())
        self.assertEqual(total_players, len(self.team.players))

    def test_depth_chart_sorted_by_rating(self):
        """Players at each position should be sorted by rating (highest first)."""
        depth_chart = self.team.depth_chart
        for position, players in depth_chart.items():
            if len(players) > 1:
                for i in range(len(players) - 1):
                    self.assertGreaterEqual(
                        players[i].rating,
                        players[i + 1].rating,
                        f"Position {position}: Player at index {i} has lower rating than player at index {i + 1}"
                    )

    def test_get_starter_returns_highest_rated(self):
        """get_starter should return the highest-rated player at a position."""
        # Test with Quarterback position
        starter = self.team.get_starter('Quarterback')
        all_qbs = [p for p in self.team.players if p.position == 'Quarterback']

        self.assertIsNotNone(starter)
        self.assertEqual(starter.position, 'Quarterback')
        # Starter should have the highest rating among all QBs
        max_rating = max(qb.rating for qb in all_qbs)
        self.assertEqual(starter.rating, max_rating)

    def test_get_starter_returns_none_for_invalid_position(self):
        """get_starter should return None for positions with no players."""
        starter = self.team.get_starter('Invalid Position')
        self.assertIsNone(starter)

    def test_get_backup_returns_correct_depth(self):
        """get_backup should return the player at the specified depth."""
        depth_chart = self.team.depth_chart

        # Test with a position that has multiple players (Wide Receiver has 8)
        position = 'Wide Receiver'
        players_at_pos = depth_chart.get(position, [])

        # Get backup at depth 2 (first backup)
        backup = self.team.get_backup(position, depth=2)
        self.assertIsNotNone(backup)
        self.assertEqual(backup, players_at_pos[1])

        # Get backup at depth 3 (second backup)
        backup_3 = self.team.get_backup(position, depth=3)
        self.assertIsNotNone(backup_3)
        self.assertEqual(backup_3, players_at_pos[2])

    def test_get_backup_default_depth_is_2(self):
        """get_backup with default depth should return the first backup."""
        depth_chart = self.team.depth_chart
        position = 'Running Back'
        players_at_pos = depth_chart.get(position, [])

        backup = self.team.get_backup(position)  # Default depth=2
        self.assertEqual(backup, players_at_pos[1])

    def test_get_backup_returns_none_for_insufficient_depth(self):
        """get_backup should return None if not enough players at position."""
        # Kicker only has 1 player
        backup = self.team.get_backup('Kicker', depth=2)
        self.assertIsNone(backup)

    def test_get_starters_returns_correct_structure(self):
        """get_starters should return dict with offense, defense, and special_teams."""
        starters = self.team.get_starters()

        self.assertIn('offense', starters)
        self.assertIn('defense', starters)
        self.assertIn('special_teams', starters)

    def test_get_starters_offense_has_11_players(self):
        """Offense starters should have 11 players total."""
        starters = self.team.get_starters()
        offense = starters['offense']

        total_offense = sum(len(players) for players in offense.values())
        self.assertEqual(total_offense, 11, "Offense should have 11 starters")

    def test_get_starters_defense_has_11_players(self):
        """Defense starters should have 11 players total."""
        starters = self.team.get_starters()
        defense = starters['defense']

        # Calculate expected defense total from config
        expected_defense = sum(DEFENSE_STARTERS.values())
        self.assertEqual(expected_defense, 11, "Defense starter config should total 11")

        total_defense = sum(len(players) for players in defense.values())
        # Defense should have all 11 starter slots filled
        self.assertEqual(total_defense, 11)

    def test_get_starters_special_teams(self):
        """Special teams should have kicker and punter."""
        starters = self.team.get_starters()
        special_teams = starters['special_teams']

        self.assertIn('Kicker', special_teams)
        self.assertIn('Punter', special_teams)
        self.assertEqual(len(special_teams['Kicker']), 1)
        self.assertEqual(len(special_teams['Punter']), 1)

    def test_starters_are_highest_rated_at_each_position(self):
        """Starters should be the highest-rated players at each position."""
        starters = self.team.get_starters()
        depth_chart = self.team.depth_chart

        # Check offense
        for position, starter_list in starters['offense'].items():
            for i, starter in enumerate(starter_list):
                expected = depth_chart[position][i]
                self.assertEqual(
                    starter, expected,
                    f"Offense starter at {position} index {i} should match depth chart"
                )

        # Check defense
        for position, starter_list in starters['defense'].items():
            for i, starter in enumerate(starter_list):
                expected = depth_chart[position][i]
                self.assertEqual(
                    starter, expected,
                    f"Defense starter at {position} index {i} should match depth chart"
                )

    def test_depth_chart_caching(self):
        """Depth chart should be cached after first access."""
        # Access depth chart twice
        chart1 = self.team.depth_chart
        chart2 = self.team.depth_chart

        # Should be the same object (cached)
        self.assertIs(chart1, chart2)

    def test_invalidate_depth_chart(self):
        """invalidate_depth_chart should rebuild the depth chart on next access."""
        # Access to build cache
        chart1 = self.team.depth_chart

        # Invalidate
        self.team.invalidate_depth_chart()

        # Access again - should be a new object
        chart2 = self.team.depth_chart

        # Should be different objects (rebuilt)
        self.assertIsNot(chart1, chart2)

    def test_offense_starter_positions(self):
        """Verify all expected offense positions are in starters."""
        starters = self.team.get_starters()
        offense = starters['offense']

        expected_positions = [
            'Quarterback', 'Running Back', 'Wide Receiver', 'Tight End',
            'Left Tackle', 'Left Guard', 'Center', 'Right Guard', 'Right Tackle'
        ]

        for position in expected_positions:
            self.assertIn(position, offense, f"Missing offense position: {position}")

    def test_defense_starter_positions(self):
        """Verify all expected defense positions are in starters."""
        starters = self.team.get_starters()
        defense = starters['defense']

        expected_positions = [
            'Edge', 'Defensive Tackle', 'Outside Linebacker', 'Middle Linebacker',
            'Cornerback', 'Free Safety', 'Strong Safety'
        ]

        for position in expected_positions:
            self.assertIn(position, defense, f"Missing defense position: {position}")


if __name__ == "__main__":
    unittest.main()
