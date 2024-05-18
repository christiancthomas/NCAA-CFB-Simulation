from game import Game

class Playoffs:
    def __init__(self, teams):
        self.teams = teams
        self.rounds = []

    def setup_playoff_bracket(self):
        # Simple 8-team playoff bracket
        self.rounds = [
            [(self.teams[0], self.teams[7]), (self.teams[3], self.teams[4])],
            [(self.teams[1], self.teams[6]), (self.teams[2], self.teams[5])]
        ]

    def play_game(self, home_team, away_team):
        game = Game(home_team.name, away_team.name)
        game.start_game()
        return game.winner

    def play_round(self, round_matches):
        next_round_teams = []
        for match in round_matches:
            winner = self.play_game(*match)
            next_round_teams.append(winner)
        return next_round_teams

    def play_playoffs(self):
        self.setup_playoff_bracket()
        round1_winners = self.play_round(self.rounds[0])
        round2_winners = self.play_round(self.rounds[1])

        semi_finalists = [*round1_winners, *round2_winners]

        final_round = [
            (semi_finalists[0], semi_finalists[3]),
            (semi_finalists[1], semi_finalists[2])
        ]

        finalists = self.play_round(final_round)
        champion = self.play_game(*finalists)

        print(f"The champion is {champion.name}")
