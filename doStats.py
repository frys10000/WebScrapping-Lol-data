import pandas as pd 
import mock


def convertDuration(gameDuration):
    '''
    Convert a string "XXm YYs" into a string list [mins, secs]
    '''
    gameDuration = gameDuration.split('m')
    gameDuration[1] = gameDuration[1][1:-1]
    return list(gameDuration)

def createChampionList(df):
    '''
    Create a dictionnary with champion as key and corresponding dataFrame as value
    '''
    df.set_index('champion').sort_values('champion')
    championList = {}
    for champion in df.champion:
        filtre = df.champion == champion
        championList[champion] =  df[filtre]

    return championList

def getWinrate(df):
    return df.win.mean()*100

def getNumberOfGames(df):
    return int(df.shape[0])

def getGold(df, gamenumber):
    return df.iloc[gamenumber].gold

def getAverageGold(df, normalize = True):
    '''
    Return the total gold earned per game 
    or if normalize = True, returns the average gold earned per 10 mins of game
    '''
    totalGold = 0
    for i in range(df.shape[0]):
        totalGold += getGold(df, i)
    return int(totalGold/(getDurations(df))) if normalize  else int(df.gold.mean())
    
def getDuration(df, gamenumber):
    '''
    Returns the duration of a game in seconds
    '''
    return int(df.iloc[gamenumber].duration[0])*60 + int(df.iloc[gamenumber].duration[1])

def getDurations(df, per10mins = True):
    '''
    Gather all the durations of a dataframe [mins, secs] and return the total duration 
    or if per10mins is set to True, the total duration / 600
    '''
    totalDuration = 0
    for i in range(df.shape[0]):
        totalDuration += getDuration(df, i)
    return totalDuration/600 if per10mins else totalDuration

def getAverageDuration(df):
    '''
    Gather all the durations of a dataframe and return the average duration over the 
    total number of entries in a tuple of int (min, sec)
    '''
    durationInSeconds = getDurations(df, False)/df.shape[0]
    durationInMinutes = int(durationInSeconds/60)
    secondsRemaining = durationInSeconds % 60
    return durationInMinutes, int(secondsRemaining)

def getAverageCs(df, normalize = True):
    '''
    Return the total gold earned per game 
    or if normalize = True, returns the average gold earned per 10 mins of game
    '''
    totalGold = 0
    for i in range(df.shape[0]):
        totalGold += df.iloc[i].cs
    return int(totalGold/(getDurations(df))) if normalize  else int(df.cs.mean())

def getDmgDone(df, gamenumber):
    return df.iloc[gamenumber].champDamage

def getAverageDmgDone(df, normalize = True):
    '''
    Return the total damage inflicted per game 
    or if normalize = True, returns the average damage inflicted per 10 mins of game
    '''
    totalDmg = 0
    for i in range(df.shape[0]):
        totalDmg += getDmgDone(df, i)
    return int(totalDmg/(getDurations(df))) if normalize else int(df.champDamage.mean())

def getDmgTaken(df, gamenumber):
    return df.iloc[gamenumber].takenDamage

def getAverageDmgTaken(df, normalize = True):
    '''
    Return the total damage taken per game 
    or if normalize = True, returns the average damage taken per 10 mins of game
    '''
    totalDmg = 0
    for i in range(df.shape[0]):
        totalDmg += getDmgTaken(df, i)
    return int(totalDmg/(getDurations(df))) if normalize else int(df.takenDamage.mean())

def printStats(dict, show_absolute = False):
        for key, value in dict.items():
            print (key, "over", getNumberOfGames(value), "game(s):")
            print("Winrate : ....................  {:.2f} %".format(getWinrate(value)))
            print("Average game duration: .......  {mins} mins {secs} secs.".format(mins= getAverageDuration(value)[0], secs= getAverageDuration(value)[1]))
            if show_absolute : print("Average gold per game: ....... ", getAverageGold(value, normalize = False))
            print("Average gold: ................ ", getAverageGold(value, normalize = True))
            if show_absolute : print("Average damage done per game:. ", getAverageDmgDone(value, normalize = False))
            print("Average damage done: ......... ", getAverageDmgDone(value, normalize = True))
            if show_absolute : print("Average damage taken per game: ", getAverageDmgDone(value, normalize = False))
            print("Average damage taken: ........ ", getAverageDmgDone(value, normalize = True))
            if show_absolute : print("Average cs per game: ......... ", getAverageCs(value, normalize = False))
            print("Average cs: .................. ", getAverageCs(value, normalize = True), '\n')

if __name__ == "__main__":
    df = pd.DataFrame.from_dict(mockStats)
    df.replace({"Victory": 1, "Defeat" : 0}, inplace= True)
    df.set_index('champion').sort_values('champion')
    df['duration'] = df["duration"].transform(convertDuration)
    printStats(createChampionList(df), show_absolute= False)
  
