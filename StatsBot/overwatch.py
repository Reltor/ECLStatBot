import json
import urllib.request
import string

characterList = {}

class Player():
    def __init__(self):
        # Comp Stats
        self.compTier = "default rank"
        self.compRank = 0
        self.compWinPercent = 00.00

        #QP & General Stats
        self.rank = 0

        #Character Stats
        self.topPlayed = "Top QP"
        self.secondPlayed = "Second QP"

        #Character Stats in Comp
        self.topPlayedComp = "Top Comp"
        self.secondPlayedComp = "Second Comp"
        
def createPlayer(battleTag):
    statData = apiQuery(battleTag)
    player = parsePlayerData(statData)
    return player

def apiQuery(battleTag):
    #take a battle tag
    #reformat battle tag for API query
 
    #some fuckery because the API hates python
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    #query owapi.net with that tag for stats
    statData = urllib.request.Request("https://owapi.net/api/v3/u/" + battleTag + "/blob",headers=headers)
    statData = urllib.request.urlopen(statData)
    statString = statData.read().decode('utf-8')
    statObject = json.loads(statString)
    #query owapi.net with that tag for hero stats
    return statObject

def parsePlayerData(statData):
    #create a blank player object
    searchedPlayer = Player()
    #insert the relevant OW data into that player
    statData = statData['us']['stats']
    qpStats = statData['quickplay']
    compStats = statData['competitive']
    searchedPlayer.battleTag

    searchedPlayer.compTier = compStats['overall_stats']['tier']
    searchedPlayer.compRank = int(compStats['overall_stats']['comprank'])
    searchedPlayer.compWinPercent = compStats['overall_stats']['win_rate']

    searchedPlayer.rank = qpStats['overall_stats']['level'] + (int(qpStats['overall_stats']['prestige'])*100)
    return searchedPlayer

def playerSummary(battleTag):
    myPlayer = createPlayer("Reltor-1266")
    #format the relevant data into a summary of the player
    summary = "Name: " + battleTag +"\n" +
              "Competitive Tier: " + myPlayer.compTier + "\n" +
              "Competitive Rank: " + str(myPlayer.compRank)
    return summary
    #return the summary as a string

def playerStat(battleTag,stat):
    #make a player object
    #take a requested stat from the user
    #compare that stat with a known list to make sure it is valid
    #if valid, return the requested stat from the player object
    pass
