import random
from team import Team

class Game:
    def __init__(self, home_name, away_name):
        self.home = Team(home_name)
        self.away = Team(away_name)
        self.home_score = 0
        self.away_score = 0
        self.current_offense = self.home
        self.current_defense = self.away
        self.ball_pos_raw = 25 # raw ball position on a scale of 0 to 100
        self.ball_pos = 25 # practical ball position - e.g. self.ball_pos_raw = 60 means self.ball_pos = 40 as 50 - abs(50-60) = 40
        self.territory = 'home' # territory is defined by self.ball_pos_raw - e.g. self.ball_pos_raw = 60 means self.territory = 'away' (ball is in away team's territory)
        self.down = 1 # play starts on first down
        self.yards_to_go = 10 # yards to first down

    def post_play(self):
        self.calc_ball_pos
        self.calc_down()
        self.score()
        return self

    def score(self):
        # ways to score:
        # ✅ 1. Touchdown (6 pts): ball crosses the goal line in opponent's territory
        # 2. Field Goal (3 pts): kicker kicks the ball through the opponent's uprights
        # 3. Post-TD Decision: Extra Point (1 pt): kicker kicks the ball through the opponent's uprights from the 2 yard line after a touchdown
        # 4. Post-TD Decision: Go for Two (2 pts): offense attempts to score again from the two yard line
        if self.ball_pos_raw >= 100 and isinstance(self.down, int):
            # home team scored TD
            self.home_score += 6
            self.down = 'PAT'
            self.ball_pos_raw = 98
            print(f'TOUCHDOWN {self.current_offense}! Score: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
        if self.ball_pos_raw <= 0 and isinstance(self.down, int):
            self.away_score += 6
            self.down = 'PAT'
            self.ball_pos_raw = 2
            print(f'TOUCHDOWN {self.current_offense}! Score: {self.home.name}: {self.home_score} - {self.away.name}: {self.away_score}')
        return self

    def turnover(self):
        print(f'{self.current_offense.name} has turned the ball over on downs.')
        if self.current_defense == self.away:
            self.current_offense = self.away
            self.current_defense = self.home
        else:
            self.current_offense = self.home
            self.current_defense = self.away
        return self

    def calc_ball_pos(self, yards_gained):
        # calculate raw ball position based on who has possession
        if self.current_offense == self.home:
            self.ball_pos_raw += yards_gained
        else:
            self.ball_pos_raw -= yards_gained
        # calculate practical ball position
        self.ball_pos = 50 - abs(self.ball_pos_raw - 50)
        if self.ball_pos_raw < 50:
            self.territory = 'home'
        elif self.ball_pos_raw == 50:
            self.territory = 'midfield'
        else:
            self.territory = 'away'
        return self

    def calc_down(self, yards_gained):
        # ✅ after the play, the amount of yards gained - yards to go = yards to go.
        # ✅ if this calculation means that yards to go <= 0, then a first down is given.
        # ✅ if a first down isn't achieved on 4th down, then it's a turnover, and the other team gets the ball
        self.yards_to_go -= yards_gained
        if self.yards_to_go <= 0:
            self.down = 1
            self.yards_to_go = 10
        elif self.yards_to_go > 0 and self.down == 4:
            self.turnover()
        else:
            self.down += 1
        return self



    def simulate_play(self, play_type):
        offense_skill = sum(player.skill_level for player in self.current_offense.players) / len(self.current_offense.players)
        defense_skill = sum(player.skill_level for player in self.current_defense.players) / len(self.current_defense.players)

        outcome = random.uniform(0, offense_skill + defense_skill)
        play_success = (outcome < offense_skill) if play_type == "run" else (outcome < (offense_skill * 0.9))

        if play_success:
            yards_gained = random.randint(1, 20)
            self.calc_ball_pos(yards_gained)
            print(f"The {play_type} play was successful! Gained {yards_gained} yards.")
        else:
            # assuming worst possible outcome of an offensive play is 0 yards
            yards_gained = 0
            print(f"The {play_type} play failed. No yards gained.")
        self.calc_down(yards_gained)
        print(f'The ball is now on the {self.ball_pos} yard line.\n {self.down} down for {self.current_offense.name}.') #TODO: buggy output

    def start_game(self):
        self.home.display_team()
        self.away.display_team()

        for _ in range(10):  # Simulate 10 plays
            play_type = input("Choose a play (r/p): ").strip().lower()
            if play_type in ["r", "p"]:
                self.simulate_play(play_type)
            else:
                print("Invalid play type. Please choose 'r' or 'p'.")
