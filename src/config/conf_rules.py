"""holds conference rule configurations:
- scheduling rules
- conference divisions
- conference championship rules
- conference bowl tie-ins"""

class Conference:
    def __init__(self):
        self.teams = 0
        self.divisions = False
        self.championship = False
        self.bowl_tie_ins = False
        self.min_games = 0
        self.max_games = 0
        self.name = None
        self.protected_rivalries = dict()

class MountainWest(Conference):
    pass

class SEC(Conference):
    pass

class Big12(Conference):
    pass

class Big10(Conference):
    pass

class American(Conference):
    pass

class SunBelt(Conference):
    pass

class Independent(Conference):
    pass

class ACC(Conference):
    """3–5–5 format, where each team plays 3 designated rivals every year along with two separate 5-team rotations 
    that flip every other year, such that every team will have at least one home game and one away game against 
    every other team in a four-year cycle (the standard length of a college player's career). Participation in the 
    ACC championship game will also no longer be determined by the winners of the two divisions; the two teams with 
    the highest conference winning percentage will play instead
    
    ACC permanent matchups (2024–present)
        School	        Rival 1	        Rival 2	        Rival 3
        Boston College	Pittsburgh	    Syracuse	
        California	    SMU	            Stanford	
        Clemson	        Florida State		
        Duke	        North Carolina	NC State	    Wake Forest
        Florida State	Clemson	        Miami	
        Georgia Tech	
        Louisville	    
        Miami	        Florida State	Virginia Tech	
        North Carolina	Duke	        NC State	    Virginia
        NC State	    Duke	        North Carolina	Wake Forest
        Pittsburgh	    Boston College	Syracuse	
        SMU	            California	    Stanford	
        Stanford	    California	    SMU	
        Syracuse	    Pittsburgh	    Boston College	
        Virginia	    North Carolina	Virginia Tech	
        Virginia Tech	Miami	        Virginia	
        Wake Forest	    Duke	        NC State"""
    
    name = 'ACC'
    teams = 15
    min_games = 8
    max_games = 8
    protected_rivalries = {
        'Boston College': ['Pittsburgh', 'Syracuse'],
        'California': ['SMU', 'Stanford'],
        'Clemson': ['Florida State'],
        'Duke': ['North Carolina', 'NC State', 'Wake Forest'],
        'Florida State': ['Clemson', 'Miami'],
        'Georgia Tech': [],
        'Louisville': [],
        'Miami': ['Florida State', 'Virginia Tech'],
        'North Carolina': ['Duke', 'NC State', 'Virginia'],
        'NC State': ['Duke', 'North Carolina', 'Wake Forest'],
        'Pittsburgh': ['Boston College', 'Syracuse'],
        'SMU': ['California', 'Stanford'],
        'Stanford': ['California', 'SMU'],
        'Syracuse': ['Pittsburgh', 'Boston College'],
        'Virginia': ['North Carolina', 'Virginia Tech'],
        'Virginia Tech': ['Miami', 'Virginia'],
        'Wake Forest': ['Duke', 'NC State']
    }
    
    def scheduler(self):
        # start each schedule by including protected rivalries
        opponents = self.protected_rivalries

        # fill out the rest of the conference schedule





class PAC12(Conference):
    pass

class MAC(Conference):
    pass

class CUSA(Conference):
    pass