# Playoff Rules

Rules governing the postseason playoff bracket. Read this before modifying `playoffs.py`.

## Format
- 8-team single-elimination bracket
- Bracket 1: Seed 1 vs 8, Seed 4 vs 5
- Bracket 2: Seed 2 vs 7, Seed 3 vs 6
- Bracket winners from each side meet in the championship game

## Seeding
- Top 8 teams by regular season record are seeded 1–8
- Tiebreaking for seeding is not yet implemented

## Game Rules
- All playoff games use the `playoff=True` flag, enabling overtime on ties
- Overtime rules follow the game overtime format (see `docs/rules/game.md`)
