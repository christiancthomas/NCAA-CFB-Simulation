import json
from src.team import Team

def load_teams_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    teams = [Team(school["School"], school["Nickname"], school["City"], school["State"], school["Enrollment"], school["Conference"]) for school in data]
    return teams
