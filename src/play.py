"""governs the rules of a single play"""
import random
import numpy as np

class Play:
    """Base class for all play types"""
    def __init__(self, offense, defense):
        self.offense = offense  # Team obj
        self.defense = defense  # Team obj
        self.yards_gained = None
        self.turnover = False
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

    def execute(self):
        """Execute the play and return yards gained"""
        raise NotImplementedError("Subclasses must implement this method")

    def _yards_gained_helper(self, phase):
        """Helper function to calculate yards gained based on phase of play."""
        if phase == 'backfield':
            return self._pick_from_bell_curve(-4, 4)
        elif phase == 'second level':
            return self._pick_from_bell_curve(2, 7)
        elif phase == 'open field':
            return self._pick_from_bell_curve(8, 99, mu=15, sigma=10)
        else:
            raise ValueError(f'{phase} is not a valid phase of play.')

    def _pick_from_bell_curve(self, min_val, max_val, mu=None, sigma=None):
        """Generate a random number from a normal distribution within a specified range"""
        if mu is None:
            mu = (max_val + min_val) / 2  # Mean of the distribution
        if sigma is None:
            sigma = abs((max_val - min_val)) / 6  # Default sigma to spread over the range

        while True:
            result = np.random.normal(mu, sigma)
            if min_val <= result <= max_val:
                return round(result)


class RunPlay(Play):
    """Represents a running play"""
    def __init__(self, offense, defense):
        super().__init__(offense, defense)

    def execute(self):
        """Execute the run play with its phases"""
        print('executing run play...')

        self.phase = 'backfield'
        self._backfield_phase()
        if self.yards_gained is not None:
            return self.yards_gained

        self.phase = 'second level'
        self._second_level_phase()
        if self.yards_gained is not None:
            return self.yards_gained

        # For now, just return a default value for the open field phase
        # TODO: Implement proper open field phase
        self.yards_gained = 25
        return self.yards_gained

    def _backfield_phase(self):
        """Executes the backfield phase of a run play"""
        print('backfield phase')
        self._engage(self.offense.get_players(position='Running Back')[0], self.phase, **self.players)

    def _second_level_phase(self):
        """Executes the second level phase of a run play"""
        print('second level phase')
        self._engage(self.offense.get_players(position='Running Back')[0], self.phase, **self.players)

    def _open_field_phase(self):
        """Executes the open field phase of a run play"""
        # TODO: Implement open field phase
        pass

    def _engage(self, ballcarrier, phase, **defenders):
        """Determines the winner of an engagement between the ballcarrier and defenders"""
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
            print(f"{[w.position+' '+ w.first_name+' '+w.last_name for w in winners]} win the interior matchup.")

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
                print(f"{[t.first_name+' '+t.last_name for t in tacklers]} are in position to make a tackle.")

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

            print(f"{[t.first_name+' '+t.last_name for t in tacklers]} are in position to make a tackle.")

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


class PassPlay(Play):
    """Represents a passing play"""
    def __init__(self, offense, defense):
        super().__init__(offense, defense)

    def execute(self):
        """Execute the pass play"""
        print('executing pass play...')

        # First determine if the pass is completed
        self._determine_pass_completion()

        if self.turnover:
            # Pass was intercepted
            return self.yards_gained or 0

        if self.yards_gained is None:
            # Pass was incomplete
            return 0

        # Pass was completed, calculate yards after catch
        self._calculate_yards_after_catch()

        return self.yards_gained

    def _determine_pass_completion(self):
        """Determines if the pass is completed, incomplete, or intercepted"""
        # TODO: Implement more comprehensive pass completion logic
        # For now, simple random completion
        qb = self.offense.get_players(position='Quarterback')[0]
        target = random.choice(self.offense.get_players(position=['Wide Receiver', 'Tight End']))
        defender = random.choice(self.defense.get_players(position=['linebacker', 'Cornerback', 'Safety']))

        # Basic completion chance based on QB and WR ratings vs DB rating
        completion_chance = (qb.rating + target.rating) / (2 * (defender.rating + 50))
        roll = random.random()

        if roll < completion_chance * 0.9:  # Completed pass
            self.yards_gained = random.randint(5, 25)
        elif roll < completion_chance * 0.93:  # Interception
            self.turnover = True
            self.yards_gained = -random.randint(0, 20)  # Return yards
        else:  # Incomplete pass
            self.yards_gained = None

    def _calculate_yards_after_catch(self):
        """Calculates yards gained after a completed catch"""
        # TODO: Implement detailed YAC logic
        # For now, just add some random yards
        if self.yards_gained is not None and not self.turnover:
            self.yards_gained += random.randint(0, 10)


def create_play(play_type, offense, defense):
    """Factory function to create appropriate play object"""
    if play_type == 'run':
        return RunPlay(offense, defense)
    elif play_type == 'pass':
        return PassPlay(offense, defense)
    else:
        raise ValueError(f'{play_type} is not a valid play type.')

