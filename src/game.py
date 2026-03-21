import random
from team import Team
from game_clock import GameClock
from game_state import GameState
from score import Score
from play import create_play  # Import the factory function
from stats import GameStats

class Game:
    """Manages a football game between two teams."""
    
    def __init__(self, home_name, away_name, playoff=False):
        """Initialize a new game between two teams."""
        self.home = Team(home_name)
        self.away = Team(away_name)
        self.score = Score()
        self.state = GameState()
        self.current_offense = self.home
        self.current_defense = self.away
        self.winner = None
        self.loser = None
        self.clock = GameClock()
        self.playoff = playoff
        self.stats = GameStats(home_name, away_name)

    def start_game(self):
        """Start and run the entire game simulation."""
        # Setup game
        self.home.display_team()
        self.away.display_team()
        self.coin_toss()
        self.state.state = 'kickoff'
        self.set_ball()

        # Main game loop
        while not self.clock.is_game_over() and not self.state.overtime:
            if self.clock.halftime:
                self.clock.end_halftime()
                self.state.state = 'halftime'
                self.set_ball()
                continue
                
            self.simulate_play(random.choice(['run', 'pass']))
                
        # Handle overtime if needed
        if self.clock.is_game_over() and self.playoff and self.score.home_score == self.score.away_score and self.state.overtime_round == 0:
            self.state.overtime = True
            self.clock.overtime = True
            self.play_ot()

        # Determine winner
        if self.score.home_score > self.score.away_score:
            self.winner = self.home
            self.loser = self.away
            print(f"{self.home.name} wins! Final Score: {self.home.name}: {self.score.home_score} - {self.away.name}: {self.score.away_score}")
        elif self.score.away_score > self.score.home_score:
            self.winner = self.away
            self.loser = self.home
            print(f"{self.away.name} wins! Final Score: {self.away.name}: {self.score.away_score} - {self.home.name}: {self.score.home_score}")
        else:
            self.tie = True
            print(f"The game ends in a tie. Final Score: {self.home.name}: {self.score.home_score} - {self.away.name}: {self.score.away_score}")

    # Coin toss and team setup
    def coin_toss(self):
        """Simulate a coin toss to determine first possession."""
        self.state.receive = random.choice([self.home, self.away])
        self.current_offense = self.state.receive
        self.state.defend = self.away if self.home == self.state.receive else self.home
        self.current_defense = self.state.defend
        return self

    # Ball position management
    def set_ball(self):
        """Set ball position based on current game state."""
        # Kickoff
        if self.state.state == 'kickoff':
            if not self.state.opening:
                self.current_offense, self.current_defense = self.current_defense, self.current_offense
            
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 25
                self.state.ball_pos = 25
            else:
                self.state.ball_pos_raw = 75
                self.state.ball_pos = 25
                
            self.state.down = 1
            self.state.yards_to_go = 10
            
            if self.state.overtime:
                self.state.state = 'overtime'
            else:
                self.state.state = 'down'
            
            self.state.opening = False
            
        # Point after touchdown
        elif self.state.state == 'pat':
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 98
            else:
                self.state.ball_pos_raw = 2
                
            self.state.down = 'PAT'
            self.state.yards_to_go = 2
            
        # Halftime transition
        elif self.state.state == 'halftime':
            self.current_offense = self.state.defend
            self.current_defense = self.state.receive
            
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 25
                self.state.ball_pos = 25
            else:
                self.state.ball_pos_raw = 75
                self.state.ball_pos = 25
                
            self.state.down = 1
            self.state.yards_to_go = 10
            self.state.state = 'down'
            
        # Overtime setup
        elif self.state.state == 'ot-reset':
            self.state.ball_pos = 25
            
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 75
            else:
                self.state.ball_pos_raw = 25
                
            self.state.state = 'overtime'
            self.state.down = 1
            self.state.yards_to_go = 10
            
        return self

    # Overtime handling
    def play_ot(self):
        """Handle overtime process."""
        # Setup overtime
        self.clock.overtime_clock()
        self.coin_toss()
        self.state.state = 'ot-reset'
        self.set_ball()
        self.state.state = 'overtime'
        print("Overtime begins!")
        self.state.overtime_round += 1
        
        # Continue playing overtime rounds until a winner is determined
        while self.state.overtime and self.score.home_score == self.score.away_score:
            # Get team order
            ball_first = self.state.receive
            ball_second = self.state.defend
            
            # First team's possession
            self.current_offense = ball_first
            self.current_defense = ball_second
            current_offense_start = self.current_offense
            
            # Run plays until turnover or score
            while self.current_offense == current_offense_start and self.state.state != 'pat':
                self.simulate_play(random.choice(['run', 'pass']))
                
            # Second team's possession
            self.current_offense = ball_second
            self.current_defense = ball_first
            current_offense_start = self.current_offense
            
            # Run plays until turnover or score
            while self.current_offense == current_offense_start and self.state.state != 'pat':
                self.simulate_play(random.choice(['run', 'pass']))
                
            # Increment overtime round
            self.state.overtime_round += 1

    # Play processing
    def simulate_play(self, play_type):
        """Simulate a single play."""
        # Guard clauses - early returns for special cases
        if self.clock.is_game_over() and not self.playoff:
            return

        if self.clock.halftime:
            self.clock.end_halftime()
            self.state.state = 'halftime'
            self.set_ball()
            return

        # Create and execute the play
        play = self._create_play(play_type, self.current_offense, self.current_defense)
        
        # Advance clock before play execution
        self.clock.resume()
        if self.state.state == 'down':
            self.clock.tick(random.randint(6, 15))

        # Execute the play
        yards_gained = play.execute()

        # Handle turnover
        if play.turnover:
            self.turnover()

        # Update game state
        self.calc_ball_pos(yards_gained)
        self.post_play(yards_gained)
        
        # Additional clock management
        if not self.clock.is_game_over() and not self.clock.halftime and not self.clock.overtime:
            if yards_gained > 0 and self.state.state == 'down':
                self.clock.tick(random.randint(10, 20))
                
        # Check for overtime
        if self.clock.is_game_over() and self.playoff and self.score.home_score == self.score.away_score and self.state.overtime_round == 0:
            self.state.overtime = True
            self.clock.overtime = True
            self.play_ot()

    def _create_play(self, play_type, offense, defense):
        """Create a play object (separated for testability)."""
        return create_play(play_type, offense, defense, stats=self.stats)

    def get_stats(self):
        """Return the game stats object."""
        return self.stats

    def get_box_score(self):
        """Return a formatted box score string."""
        lines = []
        lines.append("=" * 50)
        lines.append("BOX SCORE")
        lines.append("=" * 50)
        lines.append(f"{self.home.name}: {self.score.home_score}  -  {self.away.name}: {self.score.away_score}")
        lines.append("-" * 50)

        # Home team totals
        home_totals = self.stats.get_team_totals(self.home.name)
        lines.append(f"\n{self.home.name} Team Totals:")
        if home_totals:
            lines.append(f"  Passing: {home_totals['completions']}/{home_totals['pass_attempts']} for {home_totals['passing_yards']} yards, {home_totals['passing_tds']} TD, {home_totals['ints']} INT")
            lines.append(f"  Rushing: {home_totals['rush_attempts']} carries for {home_totals['rushing_yards']} yards, {home_totals['rushing_tds']} TD")
            lines.append(f"  Turnovers: {home_totals['fumbles'] + home_totals['ints']}")

        # Away team totals
        away_totals = self.stats.get_team_totals(self.away.name)
        lines.append(f"\n{self.away.name} Team Totals:")
        if away_totals:
            lines.append(f"  Passing: {away_totals['completions']}/{away_totals['pass_attempts']} for {away_totals['passing_yards']} yards, {away_totals['passing_tds']} TD, {away_totals['ints']} INT")
            lines.append(f"  Rushing: {away_totals['rush_attempts']} carries for {away_totals['rushing_yards']} yards, {away_totals['rushing_tds']} TD")
            lines.append(f"  Turnovers: {away_totals['fumbles'] + away_totals['ints']}")

        lines.append("\n" + "=" * 50)
        return "\n".join(lines)

    # State updates after plays
    def calc_ball_pos(self, yards_gained):
        """Calculate new ball position after yards gained/lost."""
        # Update raw ball position based on direction
        if self.current_offense == self.home:
            self.state.ball_pos_raw += yards_gained
        else:
            self.state.ball_pos_raw -= yards_gained
            
        # Calculate position relative to midfield
        self.state.ball_pos = 50 - abs(self.state.ball_pos_raw - 50)
        
        # Determine territory
        if self.state.ball_pos_raw < 50:
            self.state.territory = 'home'
        elif self.state.ball_pos_raw == 50:
            self.state.territory = 'midfield'
        else:
            self.state.territory = 'away'
            
        return self

    def post_play(self, yards_gained):
        """Update game state after a play is complete."""
        self.calc_down(yards_gained)
        self.points()
        return self

    def calc_down(self, yards_gained):
        """Calculate new down and distance after play."""
        self.state.yards_to_go -= yards_gained
        
        if self.state.yards_to_go <= 0:
            # First down
            self.state.down = 1
            self.state.yards_to_go = 10
        elif self.state.yards_to_go > 0 and self.state.down == 4:
            # Turnover on downs
            self.turnover()
            self.state.down = 1
            self.state.yards_to_go = 10
        elif self.state.state == 'pat':
            # Point after touchdown
            self.state.down = 'PAT'
        else:
            # Next down
            self.state.down += 1
            
        return self

    # Scoring logic
    def points(self):
        """Check for scoring and update points accordingly."""
        # PAT conversion
        if self.state.state == 'pat':
            if (self.current_offense == self.home and self.state.ball_pos_raw >= 100) or \
               (self.current_offense == self.away and self.state.ball_pos_raw <= 0):
                if self.current_offense == self.home:
                    self.score.home_score += 2
                else:
                    self.score.away_score += 2
                self.state.state = 'kickoff'
                
        # Regular touchdown
        elif self.state.state == 'down' and isinstance(self.state.down, int):
            if self.state.ball_pos_raw >= 100:
                self.score.home_score += 6
                self.state.ball_pos_raw = 98
                self.state.ball_pos = 2
                self.state.down = 'PAT'
                self.state.state = 'pat'
                self.clock.stop()
            elif self.state.ball_pos_raw <= 0:
                self.score.away_score += 6
                self.state.ball_pos_raw = 2
                self.state.ball_pos = 2
                self.state.down = 'PAT'
                self.state.state = 'pat'
                self.clock.stop()
                
        # Overtime scoring
        elif self.state.state == 'overtime' and isinstance(self.state.down, int):
            if self.state.ball_pos_raw >= 100:
                if self.state.overtime_round in [1, 2]:
                    self.score.home_score += 6
                    self.state.state = 'pat'
                    self.state.down = 'PAT'
                elif self.state.overtime_round >= 3:
                    self.score.home_score += 2
                    self.state.state = 'kickoff'
            elif self.state.ball_pos_raw <= 0:
                if self.state.overtime_round in [1, 2]:
                    self.score.away_score += 6
                    self.state.state = 'pat'
                    self.state.down = 'PAT'
                elif self.state.overtime_round >= 3:
                    self.score.away_score += 2
                    self.state.state = 'kickoff'
                
        self.set_ball()
        return self

    # Team possession changes
    def turnover(self):
        """Handle turnover by switching offense and defense."""
        self.current_offense, self.current_defense = self.current_defense, self.current_offense
        if self.state.overtime:
            self.state.state = 'ot-reset'
        return self

    # Utility methods
    def ordinal(self, down):
        """Convert numerical down to ordinal representation."""
        if down == 1:
            return '1st'
        elif down == 2:
            return '2nd'
        elif down == 3:
            return '3rd'
        elif down == 4:
            return '4th'
        else:
            return 'PAT'
