"""Interactive CLI for NCAA College Football Simulation."""

import os
import sys

# Ensure src/ and project root are on the path for bare imports
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_src_dir = os.path.join(_project_root, 'src')
for _p in (_project_root, _src_dir):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from utils.team_loader import load_teams_from_json
from season import Season


_DATA_PATH = os.path.join(_project_root, 'utils', 'cfb.json')


class CLI:
    """Menu-driven CLI for the college football simulator."""

    def __init__(self):
        self.season = None
        self.teams = None

    def run(self):
        """Main entry point — loops through menus until quit."""
        while True:
            action = self._main_menu()
            if action == 'quit':
                break

    # ── Menus ──────────────────────────────────────────────────────

    def _main_menu(self):
        self._clear()
        print("=" * 50)
        print("   NCAA COLLEGE FOOTBALL SIMULATOR")
        print("=" * 50)
        print()
        print("  1. Start New Season")
        print("  2. Simulate Full Season (auto-play everything)")
        print("  3. Quit")
        print()

        choice = self._get_choice("Select an option: ", range(1, 4))

        if choice == 1:
            self._start_season()
            self._weekly_loop()
        elif choice == 2:
            self._start_season()
            self._simulate_full_season()
        else:
            return 'quit'

    def _weekly_menu(self):
        """Returns an action string or None to keep looping."""
        self._clear()
        week = self.season.current_week
        print("=" * 50)
        print(f"   WEEK {week}")
        print("=" * 50)
        print()
        print("  1. View This Week's Schedule")
        print("  2. Play This Week")
        print("  3. View Last Week's Results")
        print("  4. View Standings")
        print("  5. View Top 25")
        print("  6. Team Lookup")
        print("  7. Sim Rest of Regular Season")
        print("  8. Return to Main Menu")
        print()

        choice = self._get_choice("Select an option: ", range(1, 9))

        if choice == 1:
            self._display_schedule()
        elif choice == 2:
            self._play_week()
        elif choice == 3:
            self._display_results()
        elif choice == 4:
            self._display_standings()
        elif choice == 5:
            self._display_top_25()
        elif choice == 6:
            self._team_lookup()
        elif choice == 7:
            self._sim_rest_of_season()
            return 'postseason'
        elif choice == 8:
            return 'main'

    def _postseason_menu(self):
        """Returns an action string or None to keep looping."""
        self._clear()
        print("=" * 50)
        print("   POST-SEASON")
        print("=" * 50)
        print()
        print("  1. View Final Standings")
        print("  2. View Playoff Bracket (Top 8)")
        print("  3. Run Playoffs")
        print("  4. Return to Main Menu")
        print()

        choice = self._get_choice("Select an option: ", range(1, 5))

        if choice == 1:
            self._display_standings()
        elif choice == 2:
            self._display_playoff_bracket()
        elif choice == 3:
            self._run_playoffs()
            return 'champion'
        elif choice == 4:
            return 'main'

    def _champion_screen(self):
        """Returns an action string or None to keep looping."""
        self._clear()
        print("=" * 50)
        print(f"   CHAMPION: {self.season.champion.name}")
        print("=" * 50)
        print()
        print("  1. View Final Standings")
        print("  2. New Season")
        print("  3. Quit")
        print()

        choice = self._get_choice("Select an option: ", range(1, 4))

        if choice == 1:
            self._display_standings()
        elif choice == 2:
            return 'new_season'
        elif choice == 3:
            return 'quit'

    # ── State loops ───────────────────────────────────────────────

    def _weekly_loop(self):
        while True:
            if self.season.is_regular_season_complete():
                self._postseason_loop()
                return

            action = self._weekly_menu()
            if action == 'postseason':
                self._postseason_loop()
                return
            elif action == 'main':
                return

    def _postseason_loop(self):
        while True:
            action = self._postseason_menu()
            if action == 'champion':
                self._champion_loop()
                return
            elif action == 'main':
                return

    def _champion_loop(self):
        while True:
            action = self._champion_screen()
            if action == 'new_season':
                self._start_season()
                self._weekly_loop()
                return
            elif action == 'quit':
                raise SystemExit(0)

    # ── Actions ───────────────────────────────────────────────────

    def _start_season(self):
        print("\nLoading teams and generating schedule...")
        self.teams = load_teams_from_json(_DATA_PATH)
        self.season = Season(self.teams)
        print(f"Season created with {len(self.teams)} teams.")
        self._pause()

    def _play_week(self):
        week = self.season.current_week
        if week not in self.season.schedule or not self.season.schedule[week]:
            print("\nNo games scheduled this week.")
            self._pause()
            return
        print(f"\nSimulating Week {week}...")
        self.season.play_week()
        print("Done! Games have been played.")
        self._display_results()

    def _sim_rest_of_season(self):
        print("\nSimulating remaining regular season games...")
        weeks_played = 0
        while not self.season.is_regular_season_complete():
            self.season.play_week()
            weeks_played += 1
        print(f"Simulated {weeks_played} week(s). Regular season complete!")
        self._pause()

    def _simulate_full_season(self):
        print("\nSimulating entire season and playoffs...")
        champion = self.season.simulate_full_season()
        print(f"\nSeason complete!")
        self._display_standings()
        print(f"\n{'=' * 50}")
        print(f"   CHAMPION: {champion.name}")
        print(f"{'=' * 50}")
        self._pause()

    def _run_playoffs(self):
        print()
        champion = self.season.run_playoffs()
        print()
        self._pause()

    # ── Display helpers ───────────────────────────────────────────

    def _display_schedule(self):
        week = self.season.current_week
        games = self.season.get_schedule_for_week(week)
        print(f"\n{'─' * 50}")
        print(f"  Week {week} Schedule ({len(games)} games)")
        print(f"{'─' * 50}")
        if not games:
            print("  No games scheduled.")
        else:
            for i, (home, away) in enumerate(games, 1):
                print(f"  {i:>3}. {home} vs {away}")
        self._pause()

    def _display_results(self):
        results = self.season.get_results()
        prev_week = self.season.current_week - 1
        print(f"\n{'─' * 50}")
        print(f"  Week {prev_week} Results")
        print(f"{'─' * 50}")
        if not results:
            print("  No results available.")
        else:
            for result in results:
                print(f"  {result}")
        self._pause()

    def _display_standings(self):
        standings = self.season.get_standings_sorted()
        print(f"\n{'─' * 60}")
        print(f"  {'Rank':<6}{'Team':<30}{'W':>4}{'L':>4}{'T':>4}")
        print(f"{'─' * 60}")
        for i, (team, record) in enumerate(standings, 1):
            print(f"  {i:<6}{team:<30}{record['wins']:>4}{record['losses']:>4}{record['ties']:>4}")
            if i == 25:
                print(f"{'─' * 60}")
        self._pause()

    def _display_top_25(self):
        standings = self.season.get_standings_sorted()[:25]
        print(f"\n{'─' * 60}")
        print(f"  {'Rank':<6}{'Team':<30}{'W':>4}{'L':>4}{'T':>4}")
        print(f"{'─' * 60}")
        for i, (team, record) in enumerate(standings, 1):
            print(f"  {i:<6}{team:<30}{record['wins']:>4}{record['losses']:>4}{record['ties']:>4}")
        self._pause()

    def _display_playoff_bracket(self):
        top_8 = self.season.get_top_teams(8)
        print(f"\n{'─' * 50}")
        print("  8-Team Playoff Bracket")
        print(f"{'─' * 50}")
        print(f"  Quarterfinals:")
        print(f"    (1) {top_8[0]:<20} vs  (8) {top_8[7]}")
        print(f"    (4) {top_8[3]:<20} vs  (5) {top_8[4]}")
        print(f"    (2) {top_8[1]:<20} vs  (7) {top_8[6]}")
        print(f"    (3) {top_8[2]:<20} vs  (6) {top_8[5]}")
        self._pause()

    def _team_lookup(self):
        query = input("\nEnter team name (or part of name): ").strip()
        if not query:
            return

        matches = [t for t in self.teams if query.lower() in t.name.lower()]
        if not matches:
            print(f"  No teams found matching '{query}'.")
            self._pause()
            return

        for team in matches:
            record = self.season.standings[team.name]
            print(f"\n{'─' * 50}")
            print(f"  {team.name} {team.nickname}")
            print(f"  {team.city}, {team.state} | {team.conference}")
            print(f"  Record: {record['wins']}W - {record['losses']}L - {record['ties']}T")
            print(f"\n  Starting Lineup:")
            starters = team.get_starters()
            for unit_name, unit in [('Offense', 'offense'), ('Defense', 'defense'), ('Special Teams', 'special_teams')]:
                print(f"    {unit_name}:")
                for pos, players in starters[unit].items():
                    for p in players:
                        print(f"      {pos:<22} #{p.number:<4} {p.first_name} {p.last_name} ({p.rating})")
        self._pause()

    # ── Utilities ─────────────────────────────────────────────────

    @staticmethod
    def _clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _get_choice(prompt, valid_range):
        """Prompt for an integer within valid_range, repeating on bad input."""
        while True:
            try:
                value = int(input(prompt))
                if value in valid_range:
                    return value
            except (ValueError, EOFError):
                pass
            print(f"  Please enter a number between {min(valid_range)} and {max(valid_range)}.")

    @staticmethod
    def _pause():
        input("\nPress Enter to continue...")


def main():
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main()
