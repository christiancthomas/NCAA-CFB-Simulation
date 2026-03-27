# NCAA College Football Simulator

A Python-based NCAA college football season simulator. Simulates games play-by-play, manages full seasons with conference scheduling, and runs an 8-team playoff bracket.

## Requirements

- Python 3.10+
- numpy

## Quick Start

### CLI (Interactive)

```bash
python src/cli.py
```

Or via the module entry point:

```bash
python -m src.main
```

This launches an interactive, menu-driven interface that lets you:

- **Start a new season** with all NCAA teams, auto-generated schedules, and conference play
- **Advance week by week** — view the schedule, simulate games, and check results at your own pace
- **View standings and Top 25** rankings at any point during the season
- **Look up any team** by name to see their record and full starting lineup
- **Simulate the rest of the regular season** in one step when you're ready to skip ahead
- **Run the 8-team playoff** and crown a national champion

### CLI Menu Flow

```
Main Menu → Start New Season → Weekly Menu (loop) → Post-Season Menu → Run Playoffs → Champion Screen
```

- **Weekly Menu**: View schedule, play the week, view results, standings, Top 25, team lookup, or sim the rest of the season
- **Post-Season Menu**: View final standings, preview the playoff bracket, or run the playoffs
- **Champion Screen**: View final standings, start a new season, or quit

### Simulate a Full Season (Non-Interactive)

From the main menu, select **Simulate Full Season** to auto-play the entire regular season and playoffs in one shot.

### GUI

A basic tkinter GUI is also available:

```bash
python gui.py
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
src/            Core simulation logic
  cli.py        Interactive CLI
  main.py       Module entry point
  game.py       Game engine
  play.py       Play execution (run/pass)
  season.py     Season and scheduling
  playoffs.py   8-team playoff bracket
  team.py       Team and roster management
  player.py     Player generation and ratings
  stats.py      Game statistics tracking
  config/       Conference rules and scheduling configs
utils/          Team data (cfb.json) and data loading
tests/          Pytest test suite
gui.py          Tkinter GUI
```
