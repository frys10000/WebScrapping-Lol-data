"""
Created by Laroche Alexis

On 03/05/2021 at 15:51
"""

import mainFunction as fct
from gameInfo import getPlayerGames

playerList = fct.getBestPlayer("EUW")
playerList = playerList[0:10]

allGamePlayer = {}

driver = None
for player in playerList:
    print(player, "------------------------")
    driver, allGamePlayer[player] = getPlayerGames("euw", player, 10, driver)