#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

# ---- to do list ---- nb
#   bye implementation - if count is even addPlayer
#   tie implementation -- DONE
#   cursor.execute(open("schema.sql", "r").read())
#   newstr = "".join(oldstr.split('\n'))

import psycopg2
import itertools # nb, only used if rework is implemented

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

# set dataReturn to True if you want data returned
def connect2(statement, dataReturn=False):
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(statement)
    if dataReturn:
        stuff = c.fetchall()
    else:
        db.commit()
    db.close()
    if dataReturn:
        return stuff 

def deleteMatches():
    connect2("DELETE FROM results")

def deletePlayers():
    connect2("DELETE FROM players")

def countPlayers():
    return int(connect2("SELECT COUNT(*) FROM players", True)[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) values (%s)", (name,))
    db.commit()
    db.close()

def nameFromID(playerID):
    name = connect2('select name from players where playerID=%s' % (playerID), True)
    return name[0][0]

def playerStandings(tiesEnabled=False, tourneyID=1):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

      With tiesEnabled=True tuples in list contain (id, name, wins, matches, ties, points)
      sorted by points
    """
    if tiesEnabled: 
        return connect2(open('withTies.sql', "r").read(), True)
    else: 
        return connect2(open('tester.sql', "r").read(), True)

def rework(tiesEnabled = True): # set to True for testing, nb
    ptLevels = []
    levelArray = []
    if tiesEnabled:
        standings = playerStandings(tiesEnabled)
        for player in standings:
            if player[5] not in ptLevels:
                ptLevels.append(int(player[5]))
        numLevels = len(ptLevels)
        if numLevels == 1:
            return # trivial case, all equal, just avoid repeats
        else:
            # construct Level array
            for i in range(0,numLevels):
                levelArray.append([])
            # fill level array with players
            for i in range(0,numLevels):
                for player in standings:
                    if ptLevels[i] == player[5]:
                        levelArray[i].append(player[0])
            # now that we have a lovely popluted array, get some combos!
            usableCombos = [] #nb not needed, idt
            # ptpenalty = 0 # nb, likely goes later inside loop
            # loop over pt levels, nb
            i = 0 # place holder for loop, nb
            if len(levelArray[i]) > 1:
                # holder = [] # nb, not needed yet
                starterCombos = equalPointCombos(levelArray[i])

            else:
                starterCombos = unequalPtCombos(levelArray, i) # gotta write this, nb
            # loop overStarterCombos
            s = 0 #nb, holder for loop
            # reduce working array
            # workingArray = popFromWorking(starterCombos[s], levelArray, i)
                
        return ptLevels, levelArray, starterCombos # nb, messy return for testing
    else:
        return

def rework2(tiesEndabled=True):
    ptLevels = []
    levelArray = []
    if tiesEnabled:
        standings = playerStandings(tiesEnabled)
        for player in standings:
            if player[5] not in ptLevels:
                ptLevels.append(int(player[5]))
        numLevels = len(ptLevels)
        if numLevels == 1:
            return # trivial case, all equal, just avoid repeats
        else:
            # construct Level array
            for i in range(0,numLevels):
                levelArray.append([])
            # fill level array with players
            for i in range(0,numLevels):
                for player in standings:
                    if ptLevels[i] == player[5]:
                        levelArray[i].append(player[0])
            # now that we have a lovely popluted array, get some combos!
        # start it up, nb
        if len(levelArray[0]) > 1:
            seed = equalPointCombos(levelArray[0])
    pass

def tester2():
    holder = []
    ptLevels, levelArray, starterCombos = rework()
    # assume enough levels, gotta fix, nb
    # i = 3 # nb
    for i in range(0,len(levelArray)-1): #rather count down, nb
        combos = equalPointCombos(levelArray[i] + levelArray[i+1])
        for combo in combos:
            if combo not in holder:
                holder.append(combo)
    return holder


def tester():
    holder = []
    ptLevels, levelArray, starterCombos = rework()
    # assume enough levels, gotta fix, nb
    # i = 3 # nb
    for i in range(0,len(levelArray)-1): #rather count down, nb
        combos = equalPointCombos(levelArray[i] + levelArray[i+1])
        for combo in combos:
            if combo not in holder:
                holder.append(combo)
    return holder


def tester():
    holder = []
    ptLevels, levelArray, starterCombos = rework()
    comboSize = 3
    newCombos = equalPointCombos(levelArray[0] + levelArray[1])
    mashUp = equalPointCombos(starterCombos, newCombos, 3)
    return mashUp



def getNextLevel(levelArray):
    if len(levelArray[0]) > 1:
        seed = equalPointCombos(levelArray[0])
    else:
        seed = unequalPtCombos


def equalPointCombos(singleLevel, comboSize=2):
    comboHolder = []
    combos = itertools.combinations(singleLevel, comboSize)
    for x in combos:
        comboHolder.append(x)
    return comboHolder

def unequalPtCombos(workingArray, level):
    # only one entry at level, combine with lower-adjacent
    comboHolder = []
    for entry in (workingArray[level + 1]):
        comboHolder.append((workingArray[level][0], entry))
    return comboHolder

def pfw(seed, levelArray):
    # assuming we have a seed it's either
    # one deep e.g. [(1,2), (3,4), (5,6), (7,8)]
    # or two deep 
    # get it working for one deep
    pass


def popFromWorking(starter, workingArray, level):
    workingArray[level].pop(workingArray[level].index(starter[0]))
    workingArray[level].pop(workingArray[level].index(starter[1]))
    # nb, check if len(level) = 0, if so pop
    return workingArray



def reportMatch(winner, loser, draw=False, tourneyID=1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    if winner != loser:
        db = connect()
        c = db.cursor()
        c.execute("INSERT INTO results (winner, loser, draw, tourneyID) values (%s, %s, %s, %s)", (winner, loser, draw, tourneyID))
        db.commit()
        db.close()
    else:
        print "Two players are needed for a match"
    
def swissPairings(tiesEnabled=False):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(tiesEnabled)
    # get round number, assume everyone has played 
    #   equal number of games before swissPairings can be called
    roundNumber = standings[0][3] + 1
    numMatches = countPlayers() / 2
    # generate trivial solution from standings
    #   with no dupes it's maximized 
    pairings = []
    # duplicate matchups impossible for rounds <= 2
    if roundNumber <= 2:
        for i in range(0, numMatches):
            pairings.append((standings[i*2][0], standings[i*2][1], 
                standings[i*2+1][0], standings[i*2+1][1]))
        return pairings
    # for later rounds need to check for duplicates
    else:
        bestPairTuples = getBestPairings(tiesEnabled)
        # need to get in correct format
        for pair in bestPairTuples:
            pairings.append((pair[0], nameFromID(pair[0]),
                            pair[1], nameFromID(pair[1])))
        return pairings

def makePointsDict(tiesEnabled=False):
    pts = {}
    standings = playerStandings(tiesEnabled)
    # check for ties enabled, if not
    if not tiesEnabled:
        for player in standings:
            pts[player[0]] = int(player[2]*2)
    # else, with ties enabled
    else:
        for player in standings:
            pts[player[0]] = int(player[5])
    return pts

def getBestPairings(tiesEnabled=False):
    # iniialize holder
    bestHolder = []
    results = connect2('select winner, loser from results', True)
    standings = playerStandings() # may be redundant, test removal, nb
    playerList = makePlayerList()
    ptsDict = makePointsDict()
    # create disallowed list
    disallowed = []
    for matchup in results:
        disallowed.append(matchup)
        disallowed.append((matchup[1], matchup[0]))
    for pairSet in genPairs(playerList):
        #print "back in getBestPairings" # nb
        ptDifference = 0
        for pair in pairSet:
            reverse = (pair[1], pair[0]) 
            if (pair in disallowed or reverse in disallowed):
                ptDifference += 10 # crude, should refactor
            ptDifference +=  abs(ptsDict[pair[0]] - ptsDict[pair[1]])
        if ptDifference == 0: return pairSet #, would be a good shortcut, nb
        bestHolder.append([ptDifference, pairSet])
    bestHolder.sort(key=lambda x: x[0])
    return bestHolder[0][1] #first/best one, set index
        

def makePlayerList():
    # get player list and do a bit of formatting
    playerTuples = connect2("SELECT playerID FROM players", True)
    playerList = []
    for item in playerTuples:
        playerList.append(item[0])
    return playerList

#   maybe use count players, nb
def genPairs(playerList):
    #print "called genPairs" #nb
    if len(playerList) < 2:
        yield playerList
        return
    first = playerList[0]
    for i in range(1, len(playerList)):
        pair = (first, playerList[i])
        for remainder in genPairs(playerList[1:i]+playerList[i+1:]):
            yield [pair] + remainder
