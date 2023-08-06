import pandas as pd

#Download latest data
path = 'test.csv'
df = pd.read_csv('test.csv').drop(columns = 'Unnamed: 0')

def getPlayer(name):
    """Get projected stats of specific player"""
    return df[df['Name'] == name] #Should an error be raised if the player does not exist?

def getTeam(team):
    """Get projected stats of all players from certain team"""
    return df[df['Team'] == team.upper()]

'''def scoresOver(score, fantasy):
    """Get players with scores over score based on DraftKings or FantasyDuel"""
    pass'''

def statsOver(value, stat):
    """Get players with stat values over value for a certain statistic
    (points, rebounds, assists, etc...)"""
    pass

def getInjured():
    """Get names and injury types for all injured players"""
    return df[df['Injury Indicator'] != ' ']['Name']

'''def getOptimalLineups(fantasy):
    """Get the optimal lineups for the day based on DraftKings or FantasyDuel"""
    pass'''

def getAll():
    """Get daily projections for all players"""
    return df

'''def getHistorical():
    """Get Historical Prediction data for all players"""
    pass #Is this possible to implement?'''

if __name__ == "__main__": #Test API Functions
    df = pd.read_csv('test.csv').drop(columns = 'Unnamed: 0')
    print(getPlayer('LeBron James'))
    print(getTeam('LAL'))
    print(getTeam('LAl'))
    print(getInjured())
