import pandas as pd


def position(value):
    try:
        return int(value)
    except ValueError:
        if value.startswith('T'):
            return int(value[1:])
        return value

def points(value):
    try:
        if int(value) > 0:
            return 0
        return int(value)
    except ValueError:
        return 0

def rowan_score(data):
    finish = position(data['POS'].split()[-1])
    scores = data.drop('POS')
    scores = list(map(lambda v: v.split()[1], scores))
    total = 0
    for i, score in enumerate(map(points, scores)):
        total += score * (i + 1)
    if not isinstance(finish, str):
        if finish == 1:
            total -= 10 # won
        total -= 5 # made cut

    return total

if __name__ == '__main__':
    for year in range(2004, 2022):
        df = pd.read_csv(f'RESULTS/masters_{year}.csv')
        df.columns = df.iloc[0]
        df.drop(0, axis=0, inplace=True)
        df['ROWAN SCORE'] = df[['POS', '1', '2', '3', '4']].apply(rowan_score, axis=1)
        scores = df[['PLAYER', 'ROWAN SCORE']]
        scores.columns = ['PLAYER NAME', 'ROWAN SCORE']
        scores.to_csv(f'RESULTS/rowan_{year}.csv', index=False)
