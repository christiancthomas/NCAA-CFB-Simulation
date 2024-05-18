class GameClock:
    def __init__(self):
        self.quarter = 1
        self.minutes = 15
        self.seconds = 0
        self.running = True
        self.halftime = False

    def tick(self, seconds):
        if not self.running:
            return

        self.seconds -= seconds
        while self.seconds < 0:
            self.minutes -= 1
            self.seconds += 60

        if self.minutes < 0:
            self.quarter += 1
            if self.quarter == 3:  # Indicates halftime
                self.minutes = 15
                self.seconds = 0
                self.running = True
                self.halftime = True
            elif self.quarter > 4:  # End of game
                self.minutes = 0
                self.seconds = 0
                self.running = False
            else:  # Transition between quarters
                self.minutes = 15
                self.seconds = 0

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def is_game_over(self):
        return self.quarter > 4

    # def is_halftime(self):
    #     return self.quarter == 2 and self.minutes == 0 and self.seconds == 0

    def end_halftime(self):
        self.halftime = False
        self.quarter = 3
        self.minutes = 15
        self.seconds = 0
        self.running = True

    def __str__(self):
        return f"Q{self.quarter} {self.minutes:02}:{self.seconds:02}"
