# Game Rules

Rules governing in-game simulation mechanics. Read this before modifying `game.py`, `play.py`, `game_state.py`, `game_clock.py`, or `score.py`.

## Downs and Distance
- A team has 4 downs to advance the ball 10 yards
- Gaining 10+ yards resets to 1st and 10
- Failing to convert on 4th down is a turnover on downs — possession changes and ball position flips

## Field and Ball Position
- The field is 100 yards: home team drives 0→100, away team drives 100→0
- Crossing the opponent's goal line (100 for home, 0 for away) is a touchdown
- Kickoffs place the ball at the receiving team's 25-yard line

## Scoring
- Touchdown: 6 points
- PAT (2-point conversion): 2 points, attempted from the 2-yard line after every TD
- Field goals and 1-point PATs are not yet implemented

## Clock
- 4 quarters of 15 minutes each
- Clock ticks 6–15 seconds per play, plus 10–20 seconds post-play when yards are gained
- Halftime occurs between Q2 and Q3; defending team receives the second-half kickoff
- Game ends when Q4 clock expires (unless tied in a playoff game)

## Overtime (playoff games only)
- Triggered when a playoff game is tied at the end of regulation
- Coin toss determines first possession
- Rounds 1–2: each team gets a full possession, can score TD (6 pts) + PAT (2 pts)
- Round 3+: 2-point conversion attempts only (sudden death style)
- A round ends after both teams have possessed; if still tied, a new round begins

## Play Execution
- Plays are either run or pass, created via the PlayFactory
- Run plays have three phases: backfield (DL vs OL), second level (LB/CB), open field (TODO)
- Pass plays: completion determined by QB/WR rating vs defensive rating
  - Incomplete passes have ~3% chance of interception
  - Completed passes add yards after catch (YAC)
- Yard calculations use normal distributions weighted by player ratings

## Turnovers
- Interception: occurs on failed pass completion roll (~3% chance), changes possession
- Turnover on downs: failing to convert on 4th down
- Fumbles: not yet implemented

## Coin Toss and Possession
- Pre-game coin toss randomly assigns receive/defend
- Receiving team starts on offense; defending team receives to start the second half
