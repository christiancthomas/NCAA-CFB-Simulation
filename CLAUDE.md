# CLAUDE.md

## Project Overview
NCAA College Football season simulator written in Python. Simulates games play-by-play, manages seasons with conference scheduling, and runs an 8-team playoff bracket.

## Architecture
- `src/` — Core simulation logic (game engine, plays, players, teams, seasons, playoffs, stats)
- `src/config/` — Conference rules and scheduling configurations
- `utils/` — Team data (cfb.json) and data loading utilities
- `tests/` — Pytest test suite
- `gui.py` — Tkinter-based GUI (root level)

## CI
- GitHub Actions runs pytest on push to `main`/`staging` and on PRs to `main`
- Tests run against Python 3.10, 3.11, and 3.12

## Key Commands
- **Run tests**: `python -m pytest tests/ -v`
- **Run single test file**: `python -m pytest tests/test_game.py -v`
- **Run simulation**: `python -m src.main`
- **Run GUI**: `python gui.py`

## Rules Reference
Before modifying a mechanic, read its rules doc first:
- Game simulation (`game.py`, `play.py`, `game_state.py`, `game_clock.py`, `score.py`) → `docs/rules/game.md`
- Season/scheduling (`season.py`, `src/config/conf_rules.py`) → `docs/rules/season.md`
- Playoffs (`playoffs.py`) → `docs/rules/playoffs.md`
- Recruiting (not yet implemented) → `docs/rules/recruiting.md`
- Finances (not yet implemented) → `docs/rules/finances.md`

## Pre-Commit Requirements
1. Run `python -m pytest tests/ -v` — all tests must pass
2. New or changed game mechanics in `src/` require corresponding test updates in `tests/`
3. Tests must assert behavior consistent with the rules docs above
4. User-facing changes (new features, changed behavior/output) require a README update. Internal refactors and test-only changes do not.
5. New play outcomes or stat categories must be wired into `stats.py` with a test in `test_stats.py`

## Development Guidelines
- Python >=3.10 required
- Use numpy for statistical/mathematical operations
- Test files mirror source files (e.g., `src/game.py` → `tests/test_game.py`)
- The `staging` branch is for active development; `main` is the stable branch

## Code Conventions
- Classes use PascalCase; functions/methods use snake_case
- Game simulation uses a state machine pattern (GameState tracks down, distance, position)
- Play execution uses a factory pattern (PlayFactory creates RunPlay/PassPlay)
- Player ratings are integers; yard calculations use normal distributions

## Data
- Team data lives in `utils/cfb.json` (real NCAA schools, conferences, cities, states)
- Teams are loaded via `utils/team_loader.py`
