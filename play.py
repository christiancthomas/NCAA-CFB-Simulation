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
        self.yards_gained = None
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
            - If any of the defensive linemen wins, there is a dice roll to determine which winning lineman are in position to make a tackle (high chance).
            - There is a dice roll for each lineman in position to see if they tackle the RB.
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
        Backfield	    -3 to 3         Bell Curve
        Second Level	2 to 7          Bell Curve
        Open Field	    8 to 99         Long Tail
        """
        self.phase = 'backfield'
        self._backfield_phase()
        if self.yards_gained is not None:
            return self.yards_gained
        self.phase = 'second level'
        self._second_level_phase()
        if self.yards_gained is not None:
            return self.yards_gained
        #tomporary -- delete 👇
        else:
            return 0
        # self.phase = 'open field'
        # self._open_field_phase()
        # if self.yards_gained is not None:
        #     return self.yards_gained
        # return self.yards_gained

    def _backfield_phase(self):
        """executes the backfield phase of a run play"""
        print('backfield phase')
        winners = []
        OTs = set(self.offense.get_players(position='Offensive Tackle'))
        guards = set(self.offense.get_players(position='Offensive Guard'))
        edge = set(self.offense.get_players(position='Edge'))
        DTs = list(self.defense.get_players(position='Defensive Tackle'))
        print(f"OTs: {[ ot.first_name+' '+ot.last_name for ot in OTs]},\n\
                guards: {[g.first_name+' '+g.last_name for g in guards]},\n\
                edge: {[e.first_name+' '+e.last_name for e in edge]},\n\
                    DTs: {[dt.first_name+' '+dt.last_name for dt in DTs]}\n")
        t_matchups = zip(OTs, edge)
        i_matchups = zip(guards, DTs)

        for ot, e in t_matchups:
            print(f"Offensive tackle {ot.first_name} {ot.last_name}, {ot.rating} OVR vs. Edge: {e.first_name} {e.last_name}, {e.rating} OVR")
            matchup = (ot.rating/100 * random.random() - e.rating/100 * random.random())
            print(f"dice roll result: {matchup}")
            if matchup > 0:
                print('ot wins')
                winner = ot
            elif matchup < 0:
                print('dt wins')
                winner = e
            else:
                winner = [ot, e].sort(key=lambda x: x.rating, reverse=True)[0]
            print('\n')
            winners.append(winner)

        for g, dt in i_matchups:
            print(f"Offensive guard {g.first_name} {g.last_name}, {g.rating} OVR vs. Defensive Tackle: {dt.first_name} {dt.last_name}, {dt.rating} OVR")
            matchup = (g.rating/100 * random.random() - dt.rating/100 * random.random())
            print(f"dice roll result: {matchup}")
            if matchup > 0:
                print('guard wins')
                winner = g
            elif matchup < 0:
                print('dt wins')
                winner = dt
            else:
                winner = [g, dt].sort(key=lambda x: x.rating, reverse=True)[0]
            print('\n')
            winners.append(winner)
        print(f"winners: {[winner.first_name+' '+winner.last_name for winner in winners]}")

        for winner in winners:
            # determine who gets a chance at making a tackle
            tacklers = []
            if winner in self.defense.get_players(position = ['Defensive Tackle', 'Edge']):
                # 1. calculate if the winner is in right position to make a tackle
                if random.random() < 0.8:
                    tacklers.append(winner)
        # 2. calculate if the tackler(s) makes the tackle
        if len(tacklers) != 0:
            for tackler in tacklers:
                print(f"Defensive Lineman {tackler.first_name} {tackler.last_name}, {tackler.rating} OVR vs. Running Back: {self.offense.get_players(position='Running Back')[0].first_name} {self.offense.get_players(position='Running Back')[0].last_name}, {self.offense.get_players(position='Running Back')[0].rating} OVR")
                matchup = (self.offense.get_players(position='Running Back')[0].rating/100 * random.random() - tackler.rating/100 * random.random())
                if matchup < 0:
                    print(f'{tackler.first_name} {tackler.last_name} tackles {self.offense.get_players(position='Running Back')[0].first_name} {self.offense.get_players(position='Running Back')[0].last_name}')
                    print('tackle made, calculating yards gained...')
                    self.yards_gained = self._yards_gained_helper(self.phase)
                    break
        else:
            print('no tacklers in position')
        # 3. calculate yards gained
        return self.yards_gained


    def _second_level_phase(self):
        """executes the second level phase of a run play"""
        print('second level phase')
        winners = []
        RB = self.offense.get_players(position='Running Back')[0]
        LBs = self.defense.get_players(position='Linebacker').sort(key=lambda x: x.rating, reverse=True)
        CBs = self.defense.get_players(position='Cornerback').sort(key=lambda x: x.rating, reverse=True)

        for lb in LBs:
            # 1. determine who gets a chance at making a tackle
            tacklers = []
            if random.random() < 0.5:
                tacklers.append(lb)
        # 2. calculate if the tackler(s) makes the tackle START HERE
        if len(tacklers) != 0:
            for lb in tacklers:
                print(f"Linebacker {lb.first_name} {lb.last_name}, {lb.rating} OVR vs. Running Back: {RB.first_name} {RB.last_name}, {RB.rating} OVR")
                matchup = (lb.rating/100 * random.random() - RB.rating/100 * random.random())
                print(f"dice roll result: {matchup}")
            if matchup > 0:
                print('lb wins')
                winner = lb
            elif matchup < 0:
                print('rb wins')
                winner = RB


    def _open_field_phase(self):
        ...





    ### PASS GAME ###

    def _yards_gained_helper(self, phase):
        """helper function to calculate yards gained based on phase of play.
        uses a weighted random number generator to determine yards gained.
        weights are adjusted based on phase of play.
        uses _pick_from_bell_curve() to generate random number within desired range and weighting.
        Phase	        Yards Gained    Weighting
        Backfield	    -3 to 3         Bell Curve
        Second Level	2 to 7          Bell Curve
        Open Field	    8 to 99         Long Tail"""
        # yards gained calculation
        if phase == 'backfield':
            return self._pick_from_bell_curve(-4, 4)
        elif phase == 'second level':
            return self._pick_from_bell_curve(2, 7)
        elif phase == 'open field':
            return self._pick_from_bell_curve(8, 99, mu=15, sigma=10)
        else:
            raise ValueError(f'{phase} is not a valid phase of play.')

    def _pick_from_bell_curve(self, min_val, max_val, mu=None, sigma=None):
        if mu is None:
            mu = (max_val + min_val) / 2  # Mean of the distribution
        if sigma is None:
            sigma = abs((max_val - min_val)) / 6  # Default sigma to spread over the range

        while True:
            result = np.random.normal(mu, sigma)
            if min_val <= result <= max_val:
                return round(result)
            # If result is outside the range, loop again