import random
from team import Team
from game_clock import GameClock

class Game:
    def __init__(self, home_name, away_name, playoff=False):
        self.home = Team(home_name)
        self.away = Team(away_name)
        self.home_score = 0
        self.away_score = 0
        self.current_offense = self.home
        self.current_defense = self.away
        self.ball_pos_raw = 25  # raw ball position on a scale of 0 to 100
        self.ball_pos = 25  # practical ball position
        self.territory = 'home'
        self.down = 1
        self.yards_to_go = 10
        self.state = 'down'
        self.winner = None
        self.loser = None
        self.clock = GameClock()
        self.receive = None
        self.defend = None
        self.opening = True
        self.playoff = playoff
        self.overtime = False
        self.overtime_round = 0
        self.complete_round = False

    def play_ot(self):
        self.clock.overtime_clock()
        self.coin_toss()
        self.state = 'ot-reset'
        self.set_ball()
        self.state = 'overtime'
        print("Overtime begins!")
        self.overtime_round +=1
        # Top of round
        while self.overtime and self.home_score == self.away_score:
            # run overtime loop:
            # 1. both teams get a chance to posess the ball, starting at the opponent's 25 yard line
            # 2. at the end of each OT period, we should check score -- if it's tied, we keep going, otherwise, OT ends
            # 3. no clock
            # 4. 1st OT: you just have to score a TD
            # 5. 2nd OT: you have to score a TD and attempt a 2 pt conversion
            # 6. 3rd OT+: 2 pt conversions only until a winner is found
            # while self.overtime and self.overtime_round and not self.complete_round:
            ball_first, ball_second = self.receive, self.defend
            match self.overtime_round:
                case 1:
                    while self.current_offense == ball_first:
                        # offense gets ball first
                        self.simulate_play(random.choice(['run', 'pass']))
                    # defense the gets ball
                    while self.current_offense == ball_second:
                        self.simulate_play(random.choice(['run', 'pass']))
                case 2:
                    while self.current_offense == ball_first:
                        # offense gets ball first
                        self.simulate_play(random.choice(['run', 'pass']))
                    # defense the gets ball
                    while self.current_offense == ball_second:
                        self.simulate_play(random.choice(['run', 'pass']))
                case _ if self.overtime_round >= 3:
                    while self.current_offense == ball_first:
                        # offense gets ball first
                        self.simulate_play(random.choice(['run', 'pass']))
                    # defense the gets ball
                    while self.current_offense == ball_second:
                        self.simulate_play(random.choice(['run', 'pass']))
            self.overtime_round += 1


    def coin_toss(self):
        self.receive = random.choice([self.home, self.away])
        self.current_offense = self.receive
        if self.home == self.receive:
            self.current_defense = self.away
            self.defend = self.away
        else:
            self.current_defense = self.home
            self.defend = self.home
        # print(f'{self.receive.name} has won the coin toss and has elected to receive the ball in the first half. {self.current_defense.name} will receive the ball first in the second half.')
        return self

    def kick(self):
        """method for handling field goals and PAT tries"""
        ...

    def set_ball(self):
        """method for setting the ball for special scenarios like kickoffs and PATs"""
        if self.state == 'kickoff':
            if not self.opening:
                self.current_offense, self.current_defense = self.current_defense, self.current_offense
            if self.current_offense == self.home:
                self.ball_pos_raw = 25
                self.ball_pos = 25
                self.down = 1
                self.yards_to_go = 10
            else:
                self.ball_pos_raw = 75
                self.ball_pos = 25
                self.down = 1
                self.yards_to_go = 10
            if self.overtime:
                self.state = 'overtime'
            else:
                self.state = 'down'
            self.opening = False
            # print(f'{self.ordinal(self.down)} and {self.yards_to_go} on the {self.ball_pos} yard line for {self.current_offense.name}.')

        if self.state == 'pat':
            if self.current_offense == self.home:
                self.ball_pos_raw = 98
                self.down = 'PAT'
                self.yards_to_go = 2
            else:
                self.ball_pos_raw = 2
                self.down = 'PAT'
                self.yards_to_go = 2
            # print(f'{self.ordinal(self.down)} and {self.yards_to_go} on the {self.ball_pos} yard line for {self.current_offense.name}.')

        if self.state == 'halftime':
            self.current_offense = self.defend
            self.current_defense = self.receive
            if self.current_offense == self.home:
                self.ball_pos_raw = 25
                self.ball_pos = 25
                self.down = 1
                self.yards_to_go = 10
            else:
                self.ball_pos_raw = 75
                self.ball_pos = 25
                self.down = 1
                self.yards_to_go = 10
            self.state = 'down'
            # print(f'{self.ordinal(self.down)} and {self.yards_to_go} on the {self.ball_pos} yard line for {self.current_offense.name}.')

        if self.state == 'ot-reset':
            self.ball_pos = 25 # Set ball at the 25-yard line of the opponent
            if self.current_offense == self.home:
                self.ball_pos_raw = 75
            else:
                self.ball_pos_raw = 25
            self.state = 'overtime'
            self.down = 1
        return self

    def ordinal(self, down):
        ord_dict = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 'PAT': 'PAT'}
        return ord_dict[down]

    def post_play(self, yards_gained):
        self.calc_down(yards_gained)
        self.score()
        return self

    def score(self):
        if self.state == 'pat' and self.current_offense == self.home:
            if self.ball_pos_raw >= 100:
                self.home_score += 2
                # print(f'2 point conversion is successful!\nScore: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
            # else:
                # print(f'2 point conversion is unsuccessful.\nScore: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
            self.state = 'kickoff'
        elif self.state == 'pat' and self.current_offense == self.away:
            if self.ball_pos_raw <= 0:
                self.away_score += 2
                # print(f'2 point conversion is successful!\nScore: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
            # else:
                # print(f'2 point conversion is unsuccessful.\nScore: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
            self.state = 'kickoff'
        elif self.state == 'down' and self.ball_pos_raw >= 100 and isinstance(self.down, int):
            self.home_score += 6
            # print(f'TOUCHDOWN {self.current_offense.name}! Score: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
            self.ball_pos_raw = 98
            self.ball_pos = 2
            self.down = 'PAT'
            self.state = 'pat'
            self.clock.stop()  # Stop clock for touchdown
        elif self.state == 'down' and self.ball_pos_raw <= 0 and isinstance(self.down, int):
            self.away_score += 6
            # print(f'TOUCHDOWN {self.current_offense.name}! Score: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
            self.ball_pos_raw = 2
            self.ball_pos = 2
            self.down = 'PAT'
            self.state = 'pat'
            self.clock.stop()  # Stop clock for touchdown
        if self.state == 'overtime' and self.ball_pos_raw >= 100 and isinstance(self.down, int):
            if self.overtime_round in [1, 2]:
                self.home_score += 6
                self.state = 'pat'
                self.down = 'PAT'
            elif self.overtime_round >= 3:
                self.home_score += 2
                self.state = 'kickoff'
        elif self.state == 'overtime' and self.ball_pos_raw <= 0 and isinstance(self.down, int):
            if self.overtime_round in [1, 2]:
                self.away_score += 6
                self.state = 'pat'
                self.down = 'PAT'
            elif self.overtime_round >= 3:
                self.away_score += 2
                self.state = 'kickoff'
        # if self.overtime:
        #     self.state = 'overtime'
        self.set_ball()
        return self

    def turnover(self):
        # print(f'{self.current_offense.name} has turned the ball over on downs.')
        self.current_offense, self.current_defense = self.current_defense, self.current_offense
        if self.overtime:
            self.state = 'ot-reset'
        return self

    def calc_ball_pos(self, yards_gained):
        if self.current_offense == self.home:
            self.ball_pos_raw += yards_gained
        else:
            self.ball_pos_raw -= yards_gained
        self.ball_pos = 50 - abs(self.ball_pos_raw - 50)
        if self.ball_pos_raw < 50:
            self.territory = 'home'
        elif self.ball_pos_raw == 50:
            self.territory = 'midfield'
        else:
            self.territory = 'away'
        return self

    def calc_down(self, yards_gained):
        self.yards_to_go -= yards_gained
        if self.yards_to_go <= 0:
            self.down = 1
            self.yards_to_go = 10
            # if self.state == 'down':
                # print('First down!')
        elif self.yards_to_go > 0 and self.down == 4:
            self.turnover()
            self.down = 1
            self.yards_to_go = 10
        elif self.state == 'pat':
            self.down = 'PAT'
        else:
            self.down += 1
        return self

    def simulate_play(self, play_type):
        if self.clock.is_game_over() and not self.playoff:
            return

        if self.clock.halftime:
            # print("Halftime!")
            self.clock.end_halftime()
            # print("Starting the second half!")
            self.state = 'halftime'
            self.set_ball()

        offense_skill = sum(player.skill_level for player in self.current_offense.players) / len(self.current_offense.players)
        defense_skill = sum(player.skill_level for player in self.current_defense.players) / len(self.current_defense.players)

        outcome = random.uniform(0, offense_skill + defense_skill)
        play_success = (outcome < offense_skill) if play_type == "run" else (outcome < (offense_skill * 0.9))
        self.clock.resume() # start clock again now that play has started
        if self.state == 'down':
            self.clock.tick(random.randint(6, 15))  # Tick clock for play

        if play_success:
            yards_gained = random.randint(1, 20)
            self.calc_ball_pos(yards_gained)
            # print(f"The {play_type} play was successful! Gained {yards_gained} yards.")
        else:
            yards_gained = 0
            # print(f"The {play_type} play failed. No yards gained.")
            if play_type == "pass" and not self.overtime:
                self.clock.stop()  # Stop clock for incomplete pass

        self.calc_down(yards_gained)
        self.score()
        # if isinstance(self.down, int):
            # print(f'{self.ordinal(self.down)} and {self.yards_to_go} on the {self.ball_pos} yard line for {self.current_offense.name}.')
        # else:
            # print(f'PAT for {self.current_offense.name}')

        if not self.clock.is_game_over() and not self.clock.halftime and not self.clock.overtime:
            if play_success and self.state == 'down':
                self.clock.tick(random.randint(10, 20))  # Tick clock for time between plays
            # print(f"Time remaining: {self.clock}")
        # OT check
        if self.clock.is_game_over() and self.playoff and self.home_score == self.away_score and self.overtime_round == 0:
            # enter OT
            self.overtime = True
            self.clock.overtime = True
            self.play_ot()

    def start_game(self):
        self.home.display_team()
        self.away.display_team()
        self.coin_toss()
        self.state = 'kickoff'
        self.set_ball()

        while not self.clock.is_game_over() and not self.overtime:
            if self.clock.halftime:
                # print("Halftime!")
                self.clock.end_halftime()
                # print("Starting the second half!")
                self.state = 'halftime'
                self.set_ball()
                continue
            self.simulate_play(random.choice(['run', 'pass']))
            # play_type = input("Choose a play (r/p): ").strip().lower()
            # if play_type in ["r", "p"]:
            #     self.simulate_play("run" if play_type == "r" else "pass")
            # else:
            #     self.simulate_play(random.choice(['run', 'pass']))
                # print("Invalid play type. Please choose 'r' or 'p'.")

        # print("The game is over.")
        if self.home_score > self.away_score:
            self.winner = self.home
            self.loser = self.away
            print(f"{self.home.name} wins! Final Score: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}")
        elif self.away_score > self.home_score:
            self.winner = self.away
            self.loser = self.home
            print(f"{self.away.name} wins! Final Score: {self.away.name}: {self.away_score} - {self.home.name}: {self.home_score}")
        else:
            self.tie = True
            print(f"The game ends in a tie. Final Score: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}")
