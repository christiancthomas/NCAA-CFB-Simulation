from utils.team_loader import load_teams_from_json
from season import Season

# Load teams from JSON file
teams = load_teams_from_json('cfb.json')

# Create a season
season = Season(teams)

def advance_week():
    season.play_week()

def get_current_week():
    return season.current_week

def get_week_schedule():
    return season.get_schedule_for_week(season.current_week)

def get_results():
    return season.get_results()

def get_top_teams(top_n=8):
    return season.get_top_teams(top_n)
