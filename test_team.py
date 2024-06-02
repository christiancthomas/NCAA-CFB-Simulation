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
        self.assertEqual([wr.name for wr in team.get_players(position='Wide Receiver')], 1)

    def test_update_player(self):
        team = Team("Oklahoma", "Sooners")
        if len(team.get_players(position='Quarterback')) == 1:
            qb = team.get_players(position='Quarterback') # assumes we're stil creating only one qb
        else:
            qb = team.get_players(position='Quarterback')[0]
        qb.update_player({'skill_level': 99, 'name': 'Jalen Hurts', 'number': 1})
        self.assertEqual(qb.name, 'Jalen Hurts')
        self.assertEqual(qb.skill_level, 99)
        self.assertEqual(qb.number, 1)

if __name__ == "__main__":
    unittest.main()