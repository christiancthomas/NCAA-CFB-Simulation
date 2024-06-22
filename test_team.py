from team import Team
from player import Player
import unittest

class TestTeam(unittest.TestCase):
    def test_team_creation(self):
        team = Team("Tigers")
        self.assertEqual(team.name, "Tigers")
        self.assertEqual(len(team.players), 21)

    def test_display_team(self):
        team = Team("Lions")
        # We'll just check that this method runs without error
        team.display_team()

    def test_get_player(self):
        team = Team("Red Raiders")
        self.assertEqual(len(team.get_players(position='Quarterback')), 1) # assumes we're stil creating only one qb
        self.assertEqual([wr.first_name for wr in team.get_players(position='Wide Receiver')], ['Wide Receiver', 'Wide Receiver', 'Wide Receiver'])

    def test_update_player(self):
        team = Team("Oklahoma", "Sooners")
        qb = team.get_players(position='Quarterback')[0] # assumes we're stil creating only one qb
        qb.update_player({'rating': 91, 'first_name': 'Jalen', 'last_name': 'Hurts', 'number': 1})
        self.assertEqual(qb.first_name, 'Jalen')
        self.assertEqual(qb.last_name, 'Hurts')
        self.assertEqual(qb.rating, 91)
        self.assertEqual(qb.number, 1)

if __name__ == "__main__":
    unittest.main()