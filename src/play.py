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
        self.players = {
                    'ots': self.offense.get_players(position='Offensive Tackle'),
                    'guards': self.offense.get_players(position='Offensive Guard'),
                    'centers': self.offense.get_players(position='Center'),
                    'qbs': self.offense.get_players(position='Quarterback'),
                    'rbs': self.offense.get_players(position='Running Back'),
                    'wrs': self.offense.get_players(position='Wide Receiver'),
                    'tes': self.offense.get_players(position='Tight End'),
                    'edges': self.defense.get_players(position='Edge'),
                    'dts': self.defense.get_players(position='Defensive Tackle'),
                    'lbs': self.defense.get_players(position='Linebacker'),
                    'cbs': self.defense.get_players(position='Cornerback'),
                    'safeties': self.defense.get_players(position='Safety'),
                    }
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
        """executes a run play with three phases. Uses _engage() to determine the winner of each engagement for each phase.
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
        else:
            self.phase = 'second level'
            self._second_level_phase()
        if self.yards_gained is not None:
            return self.yards_gained
        else:
            self.yards_gained = 25
            return self.yards_gained

        # if self.yards_gained is not None:
        #     return self.yards_gained
        # #tomporary -- delete 👇
        # else:
        #     return 0
        # self.phase = 'open field'
        # self._open_field_phase()
        # if self.yards_gained is not None:
        #     return self.yards_gained
        # return self.yards_gained

    def _backfield_phase(self):
        """executes the backfield phase of a run play"""
        print('backfield phase')
        self._engage(self.offense.get_players(position='Running Back')[0], self.phase, **self.players)

    def _second_level_phase(self):
        """executes the second level phase of a run play"""
        print('second level phase')
        self._engage(self.offense.get_players(position='Running Back')[0], self.phase, **self.players)

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



    def _engage(self, ballcarrier, phase, **defenders):
        """## Determines the winner of an engagement between the ballcarrier and one or more defenders.
        ### Arguments
        - ballcarrier: Player obj - the player with the ball.
        - phase: str - the phase of the play.
        - defenders: dict - a dictionary of defenders with keys for each position group.
        ### Returns
        - returns self.yards_gained if the ballcarrier is tackled.
        - returns None if the ballcarrier is not tackled.
        ### Usage details
        - uses a weighted random number generator to determine the winner.
        - weights are adjusted based on phase of play and player.
        - uses _pick_from_bell_curve() to generate random number within desired range and weighting.

        Phase	        Engagement      Weighting\n
        Backfield	    -3 to 3         Bell Curve\n
        Second Level	2 to 7          Bell Curve\n
        Open Field	    8 to 99         Long Tail"""

        winners = []
        # backfield phase
        if phase == 'backfield':
            ots, edges = defenders['ots'], defenders['edges']
            guards, dts = defenders['guards'], defenders['dts']
            o_matchups = zip(ots, edges)
            i_matchups = zip(guards, dts)

            # engage guards and dts first
            for g, dt in i_matchups:
                matchup = (g.rating/100 * random.random() - dt.rating/100 * random.random())
                if matchup > 0:
                    winner = g
                elif matchup < 0:
                    winner = dt
                else:
                    winner = [g, dt].sort(key=lambda x: x.rating, reverse=True)[0]
                winners.append(winner)

            # engage tackles and edges
            for ot, e in o_matchups:
                matchup = (ot.rating/100 * random.random() - e.rating/100 * random.random())
                if matchup > 0:
                    winner = ot
                elif matchup < 0:
                    winner = e
                else:
                    winner = [ot, e].sort(key=lambda x: x.rating, reverse=True)[0]
                winners.append(winner)

            # determine who gets a chance at making a tackle
            tacklers = []
            for winner in winners:
                if winner in self.defense.get_players(position = ['Defensive Tackle', 'Edge']):
                    # 1. calculate if the winner is in right position to make a tackle
                    if random.random() < 0.8:
                        tacklers.append(winner)
            if tacklers == []:
                print('no defenders in position to make a tackle in backfield phase')
            else:
                print(f"{[t.first_name+" "+t.last_name for t in tacklers]} are in position to make a tackle.")

            # 2. calculate if the tackler(s) makes the tackle
            if len(tacklers) != 0:
                for tackler in tacklers:
                    matchup = (ballcarrier.rating/100 * random.random() - tackler.rating/100 * random.random())
                    if matchup < 0:
                        print(f"{tackler.first_name} {tackler.last_name} makes the tackle!")
                        self.yards_gained = self._yards_gained_helper(phase)
                        return self.yards_gained
                    else:
                        print('no tackle made in backfield phase')
                        return None
            else:
                print('no defenders in position to make a tackle in backfield phase')

        # second level phase
        elif phase == 'second level':
            lbs, cbs = defenders['lbs'], defenders['cbs']

            # determine if defenders are in position to make a tackle
            tacklers = []
            for lb in lbs:
                if random.random() < 0.5:
                    tacklers.append(lb)
            for cb in cbs:
                if random.random() < 0.2:
                    tacklers.append(cb)
            print(f"{[t.first_name+" "+t.last_name for t in tacklers]} are in position to make a tackle.")
            # determine if tackler(s) make the tackle
            if len(tacklers) != 0:
                for tackler in tacklers:
                    matchup = (ballcarrier.rating/100 * random.random() - tackler.rating/100 * random.random())
                    if matchup < 0:
                        print(f"{tackler.first_name} {tackler.last_name} makes the tackle!")
                        self.yards_gained = self._yards_gained_helper(phase)
                        return self.yards_gained
            else:
                print('no tackle made in second level phase')
                return None

