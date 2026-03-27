"""Stats tracking module for NCAA CFB simulation."""


class PlayerGameStats:
    """Tracks individual player statistics for a single game.

    Stat categories by position:
    - QB: completions, attempts, passing_yards, rushing_yards, passing_tds, rushing_tds, ints, fumbles
    - RB: attempts, rushing_yards, tds, receptions, receiving_yards
    - WR/TE: receptions, receiving_yards, tds, fumbles
    - Defense: tackles, sacks, tfl, deflections, forced_fumbles, fumble_recoveries, ints, def_tds
    """

    def __init__(self):
        # QB stats
        self.completions = 0
        self.pass_attempts = 0
        self.passing_yards = 0
        self.passing_tds = 0
        self.ints = 0

        # Rushing stats (QB, RB)
        self.rush_attempts = 0
        self.rushing_yards = 0
        self.rushing_tds = 0

        # Receiving stats (RB, WR, TE)
        self.receptions = 0
        self.receiving_yards = 0
        self.receiving_tds = 0

        # Turnover stats
        self.fumbles = 0

        # Defensive stats
        self.tackles = 0
        self.sacks = 0
        self.tfl = 0  # tackles for loss
        self.deflections = 0
        self.forced_fumbles = 0
        self.fumble_recoveries = 0
        self.def_ints = 0  # defensive interceptions
        self.def_tds = 0  # defensive touchdowns

    def add_pass_attempt(self, completed=False, yards=0, td=False, intercepted=False):
        """Record a pass attempt for a QB."""
        self.pass_attempts += 1
        if completed:
            self.completions += 1
            self.passing_yards += yards
            if td:
                self.passing_tds += 1
        if intercepted:
            self.ints += 1

    def add_reception(self, yards=0, td=False):
        """Record a reception for a receiver."""
        self.receptions += 1
        self.receiving_yards += yards
        if td:
            self.receiving_tds += 1

    def add_rush(self, yards=0, td=False, fumbled=False):
        """Record a rushing attempt."""
        self.rush_attempts += 1
        self.rushing_yards += yards
        if td:
            self.rushing_tds += 1
        if fumbled:
            self.fumbles += 1

    def add_tackle(self, sack=False, tfl=False):
        """Record a tackle for a defender."""
        self.tackles += 1
        if sack:
            self.sacks += 1
        if tfl:
            self.tfl += 1

    def add_deflection(self):
        """Record a pass deflection."""
        self.deflections += 1

    def add_forced_fumble(self):
        """Record a forced fumble."""
        self.forced_fumbles += 1

    def add_fumble_recovery(self):
        """Record a fumble recovery."""
        self.fumble_recoveries += 1

    def add_interception(self, td=False):
        """Record a defensive interception."""
        self.def_ints += 1
        if td:
            self.def_tds += 1

    def add_defensive_td(self):
        """Record a defensive touchdown (fumble return, etc.)."""
        self.def_tds += 1


class GameStats:
    """Aggregates player statistics for both teams in a game."""

    def __init__(self, home_team, away_team):
        """Initialize game stats tracker.

        Args:
            home_team: Name of the home team
            away_team: Name of the away team
        """
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self._home_stats = {}  # player -> PlayerGameStats
        self._away_stats = {}  # player -> PlayerGameStats
        self._player_teams = {}  # player -> team_name (for lookup)
        self._player_info = {}  # player_key -> (full_name, position, team_name)

    def _get_or_create_stats(self, player, team_name=None):
        """Get or create PlayerGameStats for a player.

        Args:
            player: The player object
            team_name: Optional team name to register the player with

        Returns:
            PlayerGameStats for the player
        """
        # Use player's id() as key for dictionary lookup
        player_key = id(player)

        # Check if we already know this player's team
        if player_key in self._player_teams:
            team_name = self._player_teams[player_key]
        elif team_name:
            self._player_teams[player_key] = team_name

        # Record player metadata when first seen
        if player_key not in self._player_info:
            resolved_team = team_name or self._player_teams.get(player_key, "Unknown")
            number = getattr(player, 'number', '')
            name = f"{player.first_name} {player.last_name}"
            if number != '':
                name = f"#{number} {player.first_name} {player.last_name}"
            self._player_info[player_key] = (
                name,
                player.position,
                resolved_team
            )

        # Get the appropriate stats dictionary
        if team_name == self.home_team:
            if player_key not in self._home_stats:
                self._home_stats[player_key] = PlayerGameStats()
            return self._home_stats[player_key]
        elif team_name == self.away_team:
            if player_key not in self._away_stats:
                self._away_stats[player_key] = PlayerGameStats()
            return self._away_stats[player_key]
        else:
            # If no team specified, check both dictionaries
            if player_key in self._home_stats:
                return self._home_stats[player_key]
            elif player_key in self._away_stats:
                return self._away_stats[player_key]
            else:
                # Default to home team if completely unknown
                self._home_stats[player_key] = PlayerGameStats()
                self._player_teams[player_key] = self.home_team
                return self._home_stats[player_key]

    def record_pass(self, passer, target, completed, yards, intercepted=False, td=False, team_name=None):
        """Record a pass attempt.

        Args:
            passer: The QB throwing the pass
            target: The intended receiver
            completed: Whether the pass was caught
            yards: Yards gained on the play
            intercepted: Whether the pass was intercepted
            td: Whether the play resulted in a touchdown
            team_name: Optional team name for the passer
        """
        passer_stats = self._get_or_create_stats(passer, team_name)
        passer_stats.add_pass_attempt(completed=completed, yards=yards, td=td, intercepted=intercepted)

        if completed and not intercepted:
            target_stats = self._get_or_create_stats(target, team_name)
            target_stats.add_reception(yards=yards, td=td)

    def record_rush(self, carrier, yards, fumbled=False, td=False, team_name=None):
        """Record a rushing attempt.

        Args:
            carrier: The ball carrier
            yards: Yards gained on the play
            fumbled: Whether the carrier fumbled
            td: Whether the play resulted in a touchdown
            team_name: Optional team name for the carrier
        """
        carrier_stats = self._get_or_create_stats(carrier, team_name)
        carrier_stats.add_rush(yards=yards, td=td, fumbled=fumbled)

    def record_tackle(self, defender, yards_at_tackle, sack=False, tfl=False, team_name=None):
        """Record a tackle.

        Args:
            defender: The player making the tackle
            yards_at_tackle: Yards where the tackle occurred (for context)
            sack: Whether this was a sack
            tfl: Whether this was a tackle for loss
            team_name: Optional team name for the defender
        """
        defender_stats = self._get_or_create_stats(defender, team_name)
        defender_stats.add_tackle(sack=sack, tfl=tfl)

    def get_player_stats(self, player):
        """Get the stats for a specific player.

        Args:
            player: The player to get stats for

        Returns:
            PlayerGameStats for the player, or None if not found
        """
        player_key = id(player)
        if player_key in self._home_stats:
            return self._home_stats[player_key]
        elif player_key in self._away_stats:
            return self._away_stats[player_key]
        return None

    def get_team_totals(self, team_name):
        """Get aggregated statistics for a team.

        Args:
            team_name: Name of the team

        Returns:
            Dictionary with aggregated team statistics
        """
        if team_name == self.home_team:
            stats_dict = self._home_stats
        elif team_name == self.away_team:
            stats_dict = self._away_stats
        else:
            return None

        totals = {
            # Passing
            'completions': 0,
            'pass_attempts': 0,
            'passing_yards': 0,
            'passing_tds': 0,
            'ints': 0,
            # Rushing
            'rush_attempts': 0,
            'rushing_yards': 0,
            'rushing_tds': 0,
            # Receiving
            'receptions': 0,
            'receiving_yards': 0,
            'receiving_tds': 0,
            # Turnovers
            'fumbles': 0,
            # Defense
            'tackles': 0,
            'sacks': 0,
            'tfl': 0,
            'deflections': 0,
            'forced_fumbles': 0,
            'fumble_recoveries': 0,
            'def_ints': 0,
            'def_tds': 0,
        }

        for player_stats in stats_dict.values():
            totals['completions'] += player_stats.completions
            totals['pass_attempts'] += player_stats.pass_attempts
            totals['passing_yards'] += player_stats.passing_yards
            totals['passing_tds'] += player_stats.passing_tds
            totals['ints'] += player_stats.ints
            totals['rush_attempts'] += player_stats.rush_attempts
            totals['rushing_yards'] += player_stats.rushing_yards
            totals['rushing_tds'] += player_stats.rushing_tds
            totals['receptions'] += player_stats.receptions
            totals['receiving_yards'] += player_stats.receiving_yards
            totals['receiving_tds'] += player_stats.receiving_tds
            totals['fumbles'] += player_stats.fumbles
            totals['tackles'] += player_stats.tackles
            totals['sacks'] += player_stats.sacks
            totals['tfl'] += player_stats.tfl
            totals['deflections'] += player_stats.deflections
            totals['forced_fumbles'] += player_stats.forced_fumbles
            totals['fumble_recoveries'] += player_stats.fumble_recoveries
            totals['def_ints'] += player_stats.def_ints
            totals['def_tds'] += player_stats.def_tds

        return totals

    def get_player_statlines(self):
        """Return list of dicts with player info + stats for all players in this game."""
        statlines = []
        for player_key, pgs in {**self._home_stats, **self._away_stats}.items():
            name, position, team = self._player_info.get(
                player_key, ("Unknown", "Unknown", "Unknown")
            )
            statlines.append({
                'name': name, 'position': position, 'team': team, 'stats': pgs
            })
        return statlines

    def format_box_score(self):
        """Return a formatted box score string."""
        lines = []
        lines.append("=" * 60)
        lines.append("BOX SCORE")
        lines.append("=" * 60)
        lines.append(
            f"{self.home_team}: {self.home_score}  -  "
            f"{self.away_team}: {self.away_score}"
        )
        lines.append("-" * 60)

        for team_name, stats_dict in [
            (self.home_team, self._home_stats),
            (self.away_team, self._away_stats),
        ]:
            totals = self.get_team_totals(team_name)
            lines.append(f"\n{team_name} Team Totals:")
            if totals:
                lines.append(
                    f"  Passing: {totals['completions']}/{totals['pass_attempts']} "
                    f"for {totals['passing_yards']} yards, "
                    f"{totals['passing_tds']} TD, {totals['ints']} INT"
                )
                lines.append(
                    f"  Rushing: {totals['rush_attempts']} carries "
                    f"for {totals['rushing_yards']} yards, "
                    f"{totals['rushing_tds']} TD"
                )
                lines.append(
                    f"  Turnovers: {totals['fumbles'] + totals['ints']}"
                )

            # Individual player lines
            for player_key, pgs in stats_dict.items():
                name, position, _ = self._player_info.get(
                    player_key, ("Unknown", "Unknown", team_name)
                )
                parts = []
                if pgs.pass_attempts > 0:
                    parts.append(
                        f"{pgs.completions}/{pgs.pass_attempts} "
                        f"{pgs.passing_yards} pass yds, "
                        f"{pgs.passing_tds} TD, {pgs.ints} INT"
                    )
                if pgs.rush_attempts > 0:
                    parts.append(
                        f"{pgs.rush_attempts} car, "
                        f"{pgs.rushing_yards} rush yds, "
                        f"{pgs.rushing_tds} TD"
                    )
                if pgs.receptions > 0:
                    parts.append(
                        f"{pgs.receptions} rec, "
                        f"{pgs.receiving_yards} rec yds, "
                        f"{pgs.receiving_tds} TD"
                    )
                if parts:
                    lines.append(f"    {name} ({position}): {' | '.join(parts)}")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


class SeasonStats:
    """Aggregates player statistics across an entire season."""

    def __init__(self):
        self._stats = {}  # (team, name, position) -> PlayerGameStats (cumulative)
        self._player_info = {}  # (team, name, position) -> (name, position, team)

    def add_game(self, game_stats):
        """Merge a GameStats into season totals."""
        for statline in game_stats.get_player_statlines():
            key = (statline['team'], statline['name'], statline['position'])
            if key not in self._stats:
                self._stats[key] = PlayerGameStats()
                self._player_info[key] = (
                    statline['name'], statline['position'], statline['team']
                )
            self._accumulate(self._stats[key], statline['stats'])

    def _accumulate(self, target, source):
        """Add all numeric stat fields from source into target."""
        for attr in vars(source):
            val = getattr(source, attr)
            if isinstance(val, (int, float)):
                setattr(target, attr, getattr(target, attr) + val)

    def get_leaders(self, stat, top_n=10):
        """Top N players for a given stat, sorted descending."""
        entries = []
        for key, pgs in self._stats.items():
            value = getattr(pgs, stat, 0)
            if value > 0:
                name, position, team = self._player_info[key]
                entries.append({
                    'name': name,
                    'position': position,
                    'team': team,
                    'stats': pgs,
                    'value': value,
                })
        entries.sort(key=lambda e: e['value'], reverse=True)
        return entries[:top_n]
