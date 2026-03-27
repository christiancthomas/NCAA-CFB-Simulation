import test_setup
from src.stats import PlayerGameStats, GameStats, SeasonStats
from player import Player
import unittest


class TestPlayerGameStats(unittest.TestCase):
    """Tests for PlayerGameStats class."""

    def test_initialization(self):
        """Test that all stats are initialized to 0."""
        stats = PlayerGameStats()

        # QB stats
        self.assertEqual(stats.completions, 0)
        self.assertEqual(stats.pass_attempts, 0)
        self.assertEqual(stats.passing_yards, 0)
        self.assertEqual(stats.passing_tds, 0)
        self.assertEqual(stats.ints, 0)

        # Rushing stats
        self.assertEqual(stats.rush_attempts, 0)
        self.assertEqual(stats.rushing_yards, 0)
        self.assertEqual(stats.rushing_tds, 0)

        # Receiving stats
        self.assertEqual(stats.receptions, 0)
        self.assertEqual(stats.receiving_yards, 0)
        self.assertEqual(stats.receiving_tds, 0)

        # Turnover stats
        self.assertEqual(stats.fumbles, 0)

        # Defensive stats
        self.assertEqual(stats.tackles, 0)
        self.assertEqual(stats.sacks, 0)
        self.assertEqual(stats.tfl, 0)
        self.assertEqual(stats.deflections, 0)
        self.assertEqual(stats.forced_fumbles, 0)
        self.assertEqual(stats.fumble_recoveries, 0)
        self.assertEqual(stats.def_ints, 0)
        self.assertEqual(stats.def_tds, 0)

    def test_add_pass_attempt_incomplete(self):
        """Test recording an incomplete pass."""
        stats = PlayerGameStats()
        stats.add_pass_attempt(completed=False, yards=0)

        self.assertEqual(stats.pass_attempts, 1)
        self.assertEqual(stats.completions, 0)
        self.assertEqual(stats.passing_yards, 0)

    def test_add_pass_attempt_complete(self):
        """Test recording a completed pass."""
        stats = PlayerGameStats()
        stats.add_pass_attempt(completed=True, yards=15)

        self.assertEqual(stats.pass_attempts, 1)
        self.assertEqual(stats.completions, 1)
        self.assertEqual(stats.passing_yards, 15)

    def test_add_pass_attempt_td(self):
        """Test recording a passing touchdown."""
        stats = PlayerGameStats()
        stats.add_pass_attempt(completed=True, yards=45, td=True)

        self.assertEqual(stats.pass_attempts, 1)
        self.assertEqual(stats.completions, 1)
        self.assertEqual(stats.passing_yards, 45)
        self.assertEqual(stats.passing_tds, 1)

    def test_add_pass_attempt_interception(self):
        """Test recording an interception."""
        stats = PlayerGameStats()
        stats.add_pass_attempt(completed=False, yards=0, intercepted=True)

        self.assertEqual(stats.pass_attempts, 1)
        self.assertEqual(stats.completions, 0)
        self.assertEqual(stats.ints, 1)

    def test_add_reception(self):
        """Test recording a reception."""
        stats = PlayerGameStats()
        stats.add_reception(yards=20)

        self.assertEqual(stats.receptions, 1)
        self.assertEqual(stats.receiving_yards, 20)
        self.assertEqual(stats.receiving_tds, 0)

    def test_add_reception_td(self):
        """Test recording a receiving touchdown."""
        stats = PlayerGameStats()
        stats.add_reception(yards=35, td=True)

        self.assertEqual(stats.receptions, 1)
        self.assertEqual(stats.receiving_yards, 35)
        self.assertEqual(stats.receiving_tds, 1)

    def test_add_rush(self):
        """Test recording a rush."""
        stats = PlayerGameStats()
        stats.add_rush(yards=8)

        self.assertEqual(stats.rush_attempts, 1)
        self.assertEqual(stats.rushing_yards, 8)
        self.assertEqual(stats.rushing_tds, 0)
        self.assertEqual(stats.fumbles, 0)

    def test_add_rush_td(self):
        """Test recording a rushing touchdown."""
        stats = PlayerGameStats()
        stats.add_rush(yards=12, td=True)

        self.assertEqual(stats.rush_attempts, 1)
        self.assertEqual(stats.rushing_yards, 12)
        self.assertEqual(stats.rushing_tds, 1)

    def test_add_rush_fumble(self):
        """Test recording a rush with fumble."""
        stats = PlayerGameStats()
        stats.add_rush(yards=3, fumbled=True)

        self.assertEqual(stats.rush_attempts, 1)
        self.assertEqual(stats.rushing_yards, 3)
        self.assertEqual(stats.fumbles, 1)

    def test_add_tackle(self):
        """Test recording a basic tackle."""
        stats = PlayerGameStats()
        stats.add_tackle()

        self.assertEqual(stats.tackles, 1)
        self.assertEqual(stats.sacks, 0)
        self.assertEqual(stats.tfl, 0)

    def test_add_tackle_sack(self):
        """Test recording a sack."""
        stats = PlayerGameStats()
        stats.add_tackle(sack=True)

        self.assertEqual(stats.tackles, 1)
        self.assertEqual(stats.sacks, 1)

    def test_add_tackle_tfl(self):
        """Test recording a tackle for loss."""
        stats = PlayerGameStats()
        stats.add_tackle(tfl=True)

        self.assertEqual(stats.tackles, 1)
        self.assertEqual(stats.tfl, 1)

    def test_add_deflection(self):
        """Test recording a pass deflection."""
        stats = PlayerGameStats()
        stats.add_deflection()

        self.assertEqual(stats.deflections, 1)

    def test_add_forced_fumble(self):
        """Test recording a forced fumble."""
        stats = PlayerGameStats()
        stats.add_forced_fumble()

        self.assertEqual(stats.forced_fumbles, 1)

    def test_add_fumble_recovery(self):
        """Test recording a fumble recovery."""
        stats = PlayerGameStats()
        stats.add_fumble_recovery()

        self.assertEqual(stats.fumble_recoveries, 1)

    def test_add_interception(self):
        """Test recording a defensive interception."""
        stats = PlayerGameStats()
        stats.add_interception()

        self.assertEqual(stats.def_ints, 1)
        self.assertEqual(stats.def_tds, 0)

    def test_add_interception_td(self):
        """Test recording a pick-six."""
        stats = PlayerGameStats()
        stats.add_interception(td=True)

        self.assertEqual(stats.def_ints, 1)
        self.assertEqual(stats.def_tds, 1)

    def test_multiple_plays(self):
        """Test accumulating multiple plays."""
        stats = PlayerGameStats()

        # QB has a complete game
        stats.add_pass_attempt(completed=True, yards=15)
        stats.add_pass_attempt(completed=True, yards=22)
        stats.add_pass_attempt(completed=False, yards=0)
        stats.add_pass_attempt(completed=True, yards=45, td=True)
        stats.add_pass_attempt(completed=False, yards=0, intercepted=True)

        self.assertEqual(stats.pass_attempts, 5)
        self.assertEqual(stats.completions, 3)
        self.assertEqual(stats.passing_yards, 82)
        self.assertEqual(stats.passing_tds, 1)
        self.assertEqual(stats.ints, 1)


class TestGameStats(unittest.TestCase):
    """Tests for GameStats class."""

    def setUp(self):
        """Set up test fixtures."""
        self.game_stats = GameStats("Home Tigers", "Away Lions")

        # Create some test players
        self.home_qb = Player("Tom", "Brady", "Quarterback", 99, 12, side="offense")
        self.home_rb = Player("Derrick", "Henry", "Running Back", 95, 22, side="offense")
        self.home_wr = Player("Justin", "Jefferson", "Wide Receiver", 97, 18, side="offense")

        self.home_wr2 = Player("Ja'Marr", "Chase", "Wide Receiver", 96, 1, side="offense")

        self.away_qb = Player("Patrick", "Mahomes", "Quarterback", 99, 15, side="offense")
        self.away_lb = Player("Micah", "Parsons", "Linebacker", 98, 11, side="defense")

    def test_initialization(self):
        """Test GameStats initialization."""
        self.assertEqual(self.game_stats.home_team, "Home Tigers")
        self.assertEqual(self.game_stats.away_team, "Away Lions")

    def test_record_pass_complete(self):
        """Test recording a completed pass."""
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=True,
            yards=25,
            team_name="Home Tigers"
        )

        qb_stats = self.game_stats.get_player_stats(self.home_qb)
        wr_stats = self.game_stats.get_player_stats(self.home_wr)

        self.assertEqual(qb_stats.pass_attempts, 1)
        self.assertEqual(qb_stats.completions, 1)
        self.assertEqual(qb_stats.passing_yards, 25)

        self.assertEqual(wr_stats.receptions, 1)
        self.assertEqual(wr_stats.receiving_yards, 25)

    def test_record_pass_incomplete(self):
        """Test recording an incomplete pass."""
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=False,
            yards=0,
            team_name="Home Tigers"
        )

        qb_stats = self.game_stats.get_player_stats(self.home_qb)

        self.assertEqual(qb_stats.pass_attempts, 1)
        self.assertEqual(qb_stats.completions, 0)
        self.assertEqual(qb_stats.passing_yards, 0)

        # Receiver should have no stats for incomplete pass
        wr_stats = self.game_stats.get_player_stats(self.home_wr)
        self.assertIsNone(wr_stats)

    def test_record_pass_interception(self):
        """Test recording an intercepted pass."""
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=False,
            yards=0,
            intercepted=True,
            team_name="Home Tigers"
        )

        qb_stats = self.game_stats.get_player_stats(self.home_qb)

        self.assertEqual(qb_stats.pass_attempts, 1)
        self.assertEqual(qb_stats.completions, 0)
        self.assertEqual(qb_stats.ints, 1)

    def test_record_pass_td(self):
        """Test recording a passing touchdown."""
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=True,
            yards=35,
            td=True,
            team_name="Home Tigers"
        )

        qb_stats = self.game_stats.get_player_stats(self.home_qb)
        wr_stats = self.game_stats.get_player_stats(self.home_wr)

        self.assertEqual(qb_stats.passing_tds, 1)
        self.assertEqual(wr_stats.receiving_tds, 1)

    def test_record_rush(self):
        """Test recording a rush."""
        self.game_stats.record_rush(
            carrier=self.home_rb,
            yards=12,
            team_name="Home Tigers"
        )

        rb_stats = self.game_stats.get_player_stats(self.home_rb)

        self.assertEqual(rb_stats.rush_attempts, 1)
        self.assertEqual(rb_stats.rushing_yards, 12)

    def test_record_rush_td(self):
        """Test recording a rushing touchdown."""
        self.game_stats.record_rush(
            carrier=self.home_rb,
            yards=5,
            td=True,
            team_name="Home Tigers"
        )

        rb_stats = self.game_stats.get_player_stats(self.home_rb)

        self.assertEqual(rb_stats.rush_attempts, 1)
        self.assertEqual(rb_stats.rushing_yards, 5)
        self.assertEqual(rb_stats.rushing_tds, 1)

    def test_record_rush_fumble(self):
        """Test recording a fumbled rush."""
        self.game_stats.record_rush(
            carrier=self.home_rb,
            yards=3,
            fumbled=True,
            team_name="Home Tigers"
        )

        rb_stats = self.game_stats.get_player_stats(self.home_rb)

        self.assertEqual(rb_stats.rush_attempts, 1)
        self.assertEqual(rb_stats.rushing_yards, 3)
        self.assertEqual(rb_stats.fumbles, 1)

    def test_record_tackle(self):
        """Test recording a tackle."""
        self.game_stats.record_tackle(
            defender=self.away_lb,
            yards_at_tackle=5,
            team_name="Away Lions"
        )

        lb_stats = self.game_stats.get_player_stats(self.away_lb)

        self.assertEqual(lb_stats.tackles, 1)
        self.assertEqual(lb_stats.sacks, 0)
        self.assertEqual(lb_stats.tfl, 0)

    def test_record_tackle_sack(self):
        """Test recording a sack."""
        self.game_stats.record_tackle(
            defender=self.away_lb,
            yards_at_tackle=-7,
            sack=True,
            team_name="Away Lions"
        )

        lb_stats = self.game_stats.get_player_stats(self.away_lb)

        self.assertEqual(lb_stats.tackles, 1)
        self.assertEqual(lb_stats.sacks, 1)

    def test_record_tackle_tfl(self):
        """Test recording a tackle for loss."""
        self.game_stats.record_tackle(
            defender=self.away_lb,
            yards_at_tackle=-2,
            tfl=True,
            team_name="Away Lions"
        )

        lb_stats = self.game_stats.get_player_stats(self.away_lb)

        self.assertEqual(lb_stats.tackles, 1)
        self.assertEqual(lb_stats.tfl, 1)

    def test_get_player_stats_not_found(self):
        """Test getting stats for a player with no recorded plays."""
        unknown_player = Player("Unknown", "Player", "Quarterback", 50, 99)
        stats = self.game_stats.get_player_stats(unknown_player)

        self.assertIsNone(stats)

    def test_get_team_totals(self):
        """Test calculating team totals."""
        # Record some plays for home team
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=True,
            yards=25,
            team_name="Home Tigers"
        )
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=True,
            yards=15,
            td=True,
            team_name="Home Tigers"
        )
        self.game_stats.record_rush(
            carrier=self.home_rb,
            yards=10,
            team_name="Home Tigers"
        )
        self.game_stats.record_rush(
            carrier=self.home_rb,
            yards=5,
            td=True,
            team_name="Home Tigers"
        )

        totals = self.game_stats.get_team_totals("Home Tigers")

        self.assertEqual(totals['pass_attempts'], 2)
        self.assertEqual(totals['completions'], 2)
        self.assertEqual(totals['passing_yards'], 40)
        self.assertEqual(totals['passing_tds'], 1)
        self.assertEqual(totals['rush_attempts'], 2)
        self.assertEqual(totals['rushing_yards'], 15)
        self.assertEqual(totals['rushing_tds'], 1)
        self.assertEqual(totals['receptions'], 2)
        self.assertEqual(totals['receiving_yards'], 40)
        self.assertEqual(totals['receiving_tds'], 1)

    def test_get_team_totals_invalid_team(self):
        """Test getting totals for an invalid team."""
        totals = self.game_stats.get_team_totals("Invalid Team")
        self.assertIsNone(totals)

    def test_separate_team_stats(self):
        """Test that stats are tracked separately for each team."""
        # Record plays for both teams
        self.game_stats.record_pass(
            passer=self.home_qb,
            target=self.home_wr,
            completed=True,
            yards=30,
            team_name="Home Tigers"
        )
        self.game_stats.record_pass(
            passer=self.away_qb,
            target=self.away_lb,  # Using LB as a receiver for simplicity
            completed=True,
            yards=20,
            team_name="Away Lions"
        )

        home_totals = self.game_stats.get_team_totals("Home Tigers")
        away_totals = self.game_stats.get_team_totals("Away Lions")

        self.assertEqual(home_totals['passing_yards'], 30)
        self.assertEqual(away_totals['passing_yards'], 20)

    def test_qb_passes_to_two_different_receivers(self):
        """Test that a QB passing to two different WRs tracks each receiver's stats separately."""
        # QB completes two passes to WR1
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr,
            completed=True, yards=20, team_name="Home Tigers"
        )
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr,
            completed=True, yards=35, td=True, team_name="Home Tigers"
        )

        # QB completes three passes to WR2
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr2,
            completed=True, yards=10, team_name="Home Tigers"
        )
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr2,
            completed=True, yards=15, team_name="Home Tigers"
        )
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr2,
            completed=True, yards=50, td=True, team_name="Home Tigers"
        )

        # QB should have aggregate totals
        qb_stats = self.game_stats.get_player_stats(self.home_qb)
        self.assertEqual(qb_stats.pass_attempts, 5)
        self.assertEqual(qb_stats.completions, 5)
        self.assertEqual(qb_stats.passing_yards, 130)
        self.assertEqual(qb_stats.passing_tds, 2)

        # WR1 (Jefferson) — 2 catches, 55 yards, 1 TD
        wr1_stats = self.game_stats.get_player_stats(self.home_wr)
        self.assertEqual(wr1_stats.receptions, 2)
        self.assertEqual(wr1_stats.receiving_yards, 55)
        self.assertEqual(wr1_stats.receiving_tds, 1)

        # WR2 (Chase) — 3 catches, 75 yards, 1 TD
        wr2_stats = self.game_stats.get_player_stats(self.home_wr2)
        self.assertEqual(wr2_stats.receptions, 3)
        self.assertEqual(wr2_stats.receiving_yards, 75)
        self.assertEqual(wr2_stats.receiving_tds, 1)

        # Both receivers should appear as distinct entries in player statlines
        statlines = self.game_stats.get_player_statlines()
        receiver_lines = [s for s in statlines if s['position'] == 'Wide Receiver']
        self.assertEqual(len(receiver_lines), 2)
        receiver_names = {s['name'] for s in receiver_lines}
        self.assertEqual(receiver_names, {"#18 Justin Jefferson", "#1 Ja'Marr Chase"})


class TestGameStatsPlayerInfo(unittest.TestCase):
    """Tests for player metadata tracking in GameStats."""

    def setUp(self):
        self.game_stats = GameStats("Home Tigers", "Away Lions")
        self.home_qb = Player("Tom", "Brady", "Quarterback", 99, 12, side="offense")
        self.home_wr = Player("Justin", "Jefferson", "Wide Receiver", 97, 18, side="offense")
        self.away_qb = Player("Patrick", "Mahomes", "Quarterback", 99, 15, side="offense")

    def test_player_info_populated_on_record(self):
        """_player_info is populated when stats are recorded."""
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr,
            completed=True, yards=20, team_name="Home Tigers"
        )
        qb_key = id(self.home_qb)
        self.assertIn(qb_key, self.game_stats._player_info)
        name, pos, team = self.game_stats._player_info[qb_key]
        self.assertEqual(name, "#12 Tom Brady")
        self.assertEqual(pos, "Quarterback")
        self.assertEqual(team, "Home Tigers")

    def test_get_player_statlines_returns_metadata(self):
        """get_player_statlines() returns correct metadata + stats."""
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr,
            completed=True, yards=25, team_name="Home Tigers"
        )
        self.game_stats.record_rush(
            carrier=self.away_qb, yards=10, team_name="Away Lions"
        )

        statlines = self.game_stats.get_player_statlines()
        names = [s['name'] for s in statlines]
        self.assertIn("#12 Tom Brady", names)
        self.assertIn("#18 Justin Jefferson", names)
        self.assertIn("#15 Patrick Mahomes", names)

        qb_line = [s for s in statlines if s['name'] == "#12 Tom Brady"][0]
        self.assertEqual(qb_line['team'], "Home Tigers")
        self.assertEqual(qb_line['position'], "Quarterback")
        self.assertEqual(qb_line['stats'].passing_yards, 25)

    def test_format_box_score(self):
        """format_box_score() returns a non-empty string with team names."""
        self.game_stats.home_score = 21
        self.game_stats.away_score = 14
        self.game_stats.record_pass(
            passer=self.home_qb, target=self.home_wr,
            completed=True, yards=30, td=True, team_name="Home Tigers"
        )
        box = self.game_stats.format_box_score()
        self.assertIn("Home Tigers", box)
        self.assertIn("Away Lions", box)
        self.assertIn("21", box)
        self.assertIn("14", box)


class TestSeasonStats(unittest.TestCase):
    """Tests for SeasonStats class."""

    def setUp(self):
        self.season_stats = SeasonStats()
        self.qb = Player("Tom", "Brady", "Quarterback", 99, 12, side="offense")
        self.wr = Player("Justin", "Jefferson", "Wide Receiver", 97, 18, side="offense")
        self.rb = Player("Derrick", "Henry", "Running Back", 95, 22, side="offense")

    def _make_game_stats(self, team_name="Tigers"):
        """Helper to create a GameStats with some recorded plays."""
        gs = GameStats(team_name, "Opponent")
        return gs

    def test_add_game_accumulates(self):
        """add_game() accumulates stats from multiple games."""
        gs1 = self._make_game_stats()
        gs1.record_pass(self.qb, self.wr, completed=True, yards=100, team_name="Tigers")
        self.season_stats.add_game(gs1)

        gs2 = self._make_game_stats()
        gs2.record_pass(self.qb, self.wr, completed=True, yards=150, team_name="Tigers")
        self.season_stats.add_game(gs2)

        leaders = self.season_stats.get_leaders('passing_yards')
        qb_entry = [e for e in leaders if e['name'] == "#12 Tom Brady"]
        self.assertEqual(len(qb_entry), 1)
        self.assertEqual(qb_entry[0]['value'], 250)

    def test_get_leaders_sorted(self):
        """get_leaders() returns sorted results."""
        gs = self._make_game_stats()
        gs.record_pass(self.qb, self.wr, completed=True, yards=200, team_name="Tigers")
        gs.record_rush(self.rb, yards=300, team_name="Tigers")
        self.season_stats.add_game(gs)

        rushing_leaders = self.season_stats.get_leaders('rushing_yards')
        self.assertEqual(rushing_leaders[0]['name'], "#22 Derrick Henry")
        self.assertEqual(rushing_leaders[0]['value'], 300)

    def test_get_leaders_respects_top_n(self):
        """get_leaders() respects top_n parameter."""
        gs = self._make_game_stats()
        gs.record_pass(self.qb, self.wr, completed=True, yards=100, team_name="Tigers")
        gs.record_rush(self.rb, yards=50, team_name="Tigers")
        self.season_stats.add_game(gs)

        # Only ask for 1 leader
        leaders = self.season_stats.get_leaders('receiving_yards', top_n=1)
        self.assertLessEqual(len(leaders), 1)

    def test_empty_season_returns_empty_leaders(self):
        """Empty season returns empty leaders list."""
        leaders = self.season_stats.get_leaders('passing_yards')
        self.assertEqual(leaders, [])


if __name__ == "__main__":
    unittest.main()
