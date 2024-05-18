from team_loader import load_teams_from_json
from season import Season
from playoffs import Playoffs
# clean terminal for fresh
import os
os.system('cls' if os.name == 'nt' else 'clear')
# Load teams from JSON file
teams = load_teams_from_json('cfb.json')

# Play the regular season
season = Season(teams)
season.play_season()
season.display_standings()

# Determine the top 8 teams for the playoffs
top_teams = season.get_top_teams()

# Play the playoffs
playoffs = Playoffs(top_teams)
playoffs.play_playoffs()
