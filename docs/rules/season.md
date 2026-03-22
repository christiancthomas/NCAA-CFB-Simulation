# Season Rules

Rules governing season scheduling, conference play, and standings. Read this before modifying `season.py` or `src/config/conf_rules.py`.

## Schedule Structure
- Each team plays 12–14 total games per season
- 8–9 games are in-conference matchups (randomly selected from conference members)
- Remaining games are out-of-conference opponents
- No team may play more than one game per week

## Conference Rules
- Teams are assigned to conferences based on `utils/cfb.json`
- Conference-specific scheduling rules are defined in `src/config/conf_rules.py`
- ACC protected rivalries are partially defined but not yet enforced
- Division structures and conference championship games are not yet implemented

## Standings
- Standings are tracked by wins, losses, and ties
- Top 8 teams at season end qualify for the playoff
- Tiebreaking rules are not yet implemented
