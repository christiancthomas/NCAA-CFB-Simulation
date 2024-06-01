"""governs the rules of a single play"""

class Play:
    def __init__(self, offense, defense, type):
        self.offense = offense # Team obj
        self.defense = defense # Team obj
        self.yards_gained = None
        self.turnover = False
        self.type = type
        self.players = None
        self.result = None
        # stats?

    def _execute(self):
        if self.type == 'run':
            self.result = self._execute_run()
        elif self.type == 'pass':
            self.result = self._execute_pass()
        return self.result

    ### RUN GAME ###
    def _execute_run(self):
        #TODO: backfield phase
        for OT, DT in zip(self.offense.players)
    #TODO: second level phase
    #TODO: open field phase




    ### PASS GAME ###