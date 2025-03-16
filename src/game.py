import random
from team import Team
from game_clock import GameClock
from game_state import GameState
from score import Score
from play import create_play  # Import the factory function

class Game:
    def __init__(self, home_name, away_name, playoff=False):
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

    def play_ot(self):
        self.clock.overtime_clock()
        self.coin_toss()
        self.state.state = 'ot-reset'
        self.set_ball()
        self.state.state = 'overtime'
        print("Overtime begins!")
        self.state.overtime_round += 1
        # Top of round
        while self.state.overtime and self.score.home_score == self.score.away_score:
            ball_first, ball_second = self.state.receive, self.state.defend
            match self.state.overtime_round:
                case 1:
                    while self.current_offense == ball_first:
                        self.simulate_play(random.choice(['run', 'pass']))
                    while self.current_offense == ball_second:
                        self.simulate_play(random.choice(['run', 'pass']))
                case 2:
                    while self.current_offense == ball_first:
                        self.simulate_play(random.choice(['run', 'pass']))
                    while self.current_offense == ball_second:
                        self.simulate_play(random.choice(['run', 'pass']))
                case _ if self.state.overtime_round >= 3:
                    while self.current_offense == ball_first:
                        self.simulate_play(random.choice(['run', 'pass']))
                    while self.current_offense == ball_second:
                        self.simulate_play(random.choice(['run', 'pass']))
            self.state.overtime_round += 1

    def coin_toss(self):
        self.state.receive = random.choice([self.home, self.away])
        self.current_offense = self.state.receive
        if self.home == self.state.receive:
            self.current_defense = self.away
            self.state.defend = self.away
        else:
            self.current_defense = self.home
            self.state.defend = self.home
        return self

    def kick(self):
        """method for handling field goals and PAT tries"""
        ...

    def set_ball(self):
        if self.state.state == 'kickoff':
            if not self.state.opening:
                self.current_offense, self.current_defense = self.current_defense, self.current_offense
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 25
                self.state.ball_pos = 25
                self.state.down = 1
                self.state.yards_to_go = 10
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

        if self.state.state == 'pat':
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 98
                self.state.down = 'PAT'
                self.state.yards_to_go = 2
            else:
                self.state.ball_pos_raw = 2
                self.state.down = 'PAT'
                self.state.yards_to_go = 2

        if self.state.state == 'halftime':
            self.current_offense = self.state.defend
            self.current_defense = self.state.receive
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 25
                self.state.ball_pos = 25
                self.state.down = 1
                self.state.yards_to_go = 10
            else:
                self.state.ball_pos_raw = 75
                self.state.ball_pos = 25
                self.state.down = 1
                self.state.yards_to_go = 10
            self.state.state = 'down'

        if self.state.state == 'ot-reset':
            self.state.ball_pos = 25
            if self.current_offense == self.home:
                self.state.ball_pos_raw = 75
            else:
                self.state.ball_pos_raw = 25
            self.state.state = 'overtime'
            self.state.down = 1
        return self

    def ordinal(self, down):
        ord_dict = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 'PAT': 'PAT'}
        return ord_dict[down]

    def post_play(self, yards_gained):
        self.calc_down(yards_gained)
        self.score()
        return self

    def score(self):
        if self.state.state == 'pat' and self.current_offense == self.home:
            if self.state.ball_pos_raw >= 100:
                self.score.home_score += 2
            self.state.state = 'kickoff'
        elif self.state.state == 'pat' and self.current_offense == self.away:
            if self.state.ball_pos_raw <= 0:
                self.score.away_score += 2
            self.state.state = 'kickoff'
        elif self.state.state == 'down' and self.state.ball_pos_raw >= 100 and isinstance(self.state.down, int):
            self.score.home_score += 6
            self.state.ball_pos_raw = 98
            self.state.ball_pos = 2
            self.state.down = 'PAT'
            self.state.state = 'pat'
            self.clock.stop()
        elif self.state.state == 'down' and self.state.ball_pos_raw <= 0 and isinstance(self.state.down, int):
            self.score.away_score += 6
            self.state.ball_pos_raw = 2
            self.state.ball_pos = 2
            self.state.down = 'PAT'
            self.state.state = 'pat'
            self.clock.stop()
        if self.state.state == 'overtime' and self.state.ball_pos_raw >= 100 and isinstance(self.state.down, int):
            if self.state.overtime_round in [1, 2]:
                self.score.home_score += 6
                self.state.state = 'pat'
                self.state.down = 'PAT'
            elif self.state.overtime_round >= 3:
                self.score.home_score += 2
                self.state.state = 'kickoff'
        elif self.state.state == 'overtime' and self.state.ball_pos_raw <= 0 and isinstance(self.state.down, int):
            if self.state.overtime_round in [1, 2]:
                self.score.away_score += 6
                self.state.state = 'pat'
                self.state.down = 'PAT'
            elif self.state.overtime_round >= 3:
                self.score.away_score += 2
                self.state.state = 'kickoff'
        self.set_ball()
        return self

    def turnover(self):
        self.current_offense, self.current_defense = self.current_defense, self.current_offense
        if self.state.overtime:
            self.state.state = 'ot-reset'
        return self

    def calc_ball_pos(self, yards_gained):
        if self.current_offense == self.home:
            self.state.ball_pos_raw += yards_gained
        else:
            self.state.ball_pos_raw -= yards_gained
        self.state.ball_pos = 50 - abs(self.state.ball_pos_raw - 50)
        if self.state.ball_pos_raw < 50:
            self.state.territory = 'home'
        elif self.state.ball_pos_raw == 50:
            self.state.territory = 'midfield'
        else:
            self.state.territory = 'away'
        return self

    def calc_down(self, yards_gained):
        self.state.yards_to_go -= yards_gained
        if self.state.yards_to_go <= 0:
            self.state.down = 1
            self.state.yards_to_go = 10
        elif self.state.yards_to_go > 0 and self.state.down == 4:
            self.turnover()
            self.state.down = 1
            self.state.yards_to_go = 10
        elif self.state.state == 'pat':
            self.state.down = 'PAT'
        else:
            self.state.down += 1
        return self

    def simulate_play(self, play_type):
        """Use the Play class hierarchy to simulate plays"""
        if self.clock.is_game_over() and not self.playoff:
            return

        if self.clock.halftime:
            self.clock.end_halftime()
            self.state.state = 'halftime'
            self.set_ball()
            return

        # Create a play object using the factory function
        play = create_play(play_type, self.current_offense, self.current_defense)

        # Execute the play and get the yards gained
        self.clock.resume()
        if self.state.state == 'down':
            self.clock.tick(random.randint(6, 15))

        yards_gained = play.execute()

        # Handle turnover if it happened
        if play.turnover:
            self.turnover()

        # Update game state based on play results
        self.calc_ball_pos(yards_gained)
        self.calc_down(yards_gained)
        self.score()

        # Additional clock management
        if not self.clock.is_game_over() and not self.clock.halftime and not self.clock.overtime:
            if yards_gained > 0 and self.state.state == 'down':
                self.clock.tick(random.randint(10, 20))

        # Check for overtime
        if self.clock.is_game_over() and self.playoff and self.score.home_score == self.score.away_score and self.state.overtime_round == 0:
            self.state.overtime = True
            self.clock.overtime = True
            self.play_ot()

    def start_game(self):
        self.home.display_team()
        self.away.display_team()
        self.coin_toss()
        self.state.state = 'kickoff'
        self.set_ball()

        while not self.clock.is_game_over() and not self.state.overtime:
            if self.clock.halftime:
                self.clock.end_halftime()
                self.state.state = 'halftime'
                self.set_ball()
                continue
            self.simulate_play(random.choice(['run', 'pass']))

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
