"""governs the rules of a single play"""
import random
import numpy as np

class Play:
    def __init__(self, offense, defense, type):
        self.offense = offense # Team obj
        self.defense = defense # Team obj
        self.yards_gained = None
        self.turnover = False
        self.type = type
        self.players = None
        self.result = None
        self.phase = None
        # stats?
        self._execute()

    def _execute(self):
        print('executing play...')
        print(self.type)
        if self.type == 'run':
            self.result = self._execute_run()
        elif self.type == 'pass':
            self.result = self._execute_pass()
        else: 
            raise ValueError(f'{self.type} is not a valid play type.')
        return self.result

    ### RUN GAME ###
    def _execute_run(self):
        """executes a run play with three phases
        1. backfield phase: QB hands off to RB. 
            - There is a dice roll to determine who wins each blocking engagement.
            - If any of the defensive linemen wins, there is a dice roll for each one to see if they tackle the RB.
            - If the RB wins the engagement(s), they advance to the second level phase.
            - If the RB loses any engagement(s), the play is over.
        2. second level phase: RB advances past the line of scrimmage and is now engaging with linebackers and cornerbacks.
            - There is a dice roll to see which linebacker(s) (medium chance) and cornerbacks (low chance) are in the correct position to make a tackle.
            - For linebackers in position, there is a dice roll to see if they make the tackle.
            - If the RB wins the engagement(s), they advance to the open field phase.
        3. open field phase: RB is in the open field and is now engaging with safeties.
            - There is a dice roll to see which safeties are in the correct position to make a tackle (medium chance).
            - For safeties in position, there is a dice roll to see if they make the tackle.
            - If the RB wins the engagement(s), they advance the ball to the end zone.
        If the RB is tackled at any point, yards gained are calculated and the play is over.
        Yards gained for the backfield and second level phase are weighted on a bell curve distribution.
        Yards gained for the open field phase are distributed on a very long tail distribution such that very few open field pays will result in huge gains.
        Yards gained are calculated based on the phase of the play in which the tackle occurred and the rules can be found in the table below:
        Phase	        Yards Gained    Weighting
        Backfield	    -5 to 2         Bell Curve
        Second Level	3 to 6          Bell Curve
        Open Field	    7 to 99         Long Tail
        """
        self.phase = 'backfield'
        print('backfield phase')
        winners = []
        # backfield phase
        OTs = set(self.offense.get_players(position='Offensive Tackle'))
        guards = set(self.offense.get_players(position='Offensive Guard'))
        edge = set(self.offense.get_players(position='Edge'))
        DTs = list(self.defense.get_players(position='Defensive Tackle'))
        # make matchups between individual tackles and edges as well as guards and d tackles
        t_matchups = zip(OTs, DTs)
        print(f"t_matchups: {t_matchups}")
        i_matchups = zip(guards, DTs)
        print(f"i_matchups: {i_matchups}")
        for ot, e in t_matchups:
            print(f"OT: {ot}, Edge: {e}")
            # dice roll
            matchup = (ot.rating/100 * random.random() - e.rating/100 * random.random())
            if matchup > 0:
                print('ot wins')
                winner = ot
            elif matchup < 0:
                print('dt wins')
                winner = e
            else:
                winner = [ot, e].sort(key=lambda x: x.rating, reverse=True)[0]
            winners.append(winner)
        for g, dt in i_matchups:
            print(f"g: {g}, dt: {dt}")
            matchup = (g.rating/100 * random.random() - dt.rating/100 * random.random())
            if matchup > 0:
                print('guard wins')
                winner = g
            elif matchup < 0:
                print('dt wins')
                winner = dt
            else:
                winner = [g, dt].sort(key=lambda x: x.rating, reverse=True)[0]
            winners.append(winner)
        print(f"winners: {winners}")
        # check for defensive linemen winners
        for winner in winners:
            if winner in DTs:
                print('dt wins')
                # matchup challenge to see if they tackle the RB
                matchup = (self.offense.get_players(position='Running Back')[0].rating/100 * random.random() - winner.rating/100 * random.random())
                if matchup < 0:
                    print('dt tackles rb')
                    

                




    ### PASS GAME ###

    def _yards_gained_helper(self, phase):
        """helper function to calculate yards gained based on phase of play.
        uses a weighted random number generator to determine yards gained.
        weights are adjusted based on phase of play.
        uses _pick_from_bell_curve() to generate random number within desired range and weighting.
        Phase	        Yards Gained    Weighting
        Backfield	    -5 to 2         Bell Curve
        Second Level	3 to 6          Bell Curve
        Open Field	    7 to 99         Long Tail"""
        # yards gained calculation
        if phase == 'backfield':
            return self._pick_from_bell_curve(-5, 2)
        elif phase == 'second level':
            return self._pick_from_bell_curve(3, 6)
        elif phase == 'open field':
            return self._pick_from_bell_curve(7, 99, mu=15, sigma=10)
        else:
            raise ValueError(f'{phase} is not a valid phase of play.')
    
    def _pick_from_bell_curve(min_val, max_val, mu=None, sigma=None):
        if mu is None:
            mu = (max_val + min_val) / 2  # Mean of the distribution
        if sigma is None:
            sigma = (max_val - min_val) / 6  # Default sigma to spread over the range
        
        while True:
            result = np.random.normal(mu, sigma)
            if min_val <= result <= max_val:
                return round(result)
            # If result is outside the range, loop again