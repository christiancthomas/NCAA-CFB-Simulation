class GameState:
    def __init__(self):
        self.ball_pos_raw = 25  # raw ball position on a scale of 0 to 100
        self.ball_pos = 25  # practical ball position
        self.territory = 'home'
        self.down = 1
        self.yards_to_go = 10
        self.state = 'down'
        self.receive = None
        self.defend = None
        self.opening = True
        self.overtime = False
        self.overtime_round = 0
        self.complete_round = False
        self.play_success = False
