# Prediction of golfer performance for a Masters pool

Using regression models to predict a players score given the rules of the pool.

The rules are as follows:
- A team consists of 11 players:
  - 3 ranked 1 - 15 in the world
  - 3 ranked 16 - 30 in the world
  - 3 ranked 31 or below
  - 1 amatuer
  - 1 (unranked) past champion
- Round 1: Players who shoot under par will receive 1 point per stroke under par.
- Round 2: Players who shoot under par will receive 2 points per stroke under par.
  An additional 5 points will be awarded for each player making the cut
- Round 3: Players who shoot under par will receive 3 points per stroke under par.
- Round 4: Players who shoot under par will receive 4 points per stroke under par.
  The winner of the tournament receives 10 additional points.

  These scores were calculated for all Masters tournaments from 2004 to 2021.
