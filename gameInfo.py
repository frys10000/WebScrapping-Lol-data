# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:05:42 2021

@author: android01
"""

import time, re

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (NoSuchElementException, 
                                        TimeoutException, 
                                        WebDriverException)

firefoxDriver = "webDriver/geckodriver.exe"
chromeDriver = "webDriver/chromedriver.exe"


def getDriver(usingChrome = False, usingFirefox = False):
    """
    Initialise le driver de Chrome ou Firefox
    Renvoie None si aucun des deux n'a été initialisé
    """
    if usingChrome:
        try:
            driver = Chrome(executable_path = chromeDriver)
            return driver
        
        except WebDriverException:
            print("Failed to initialize Chrome driver")
        
    if usingFirefox:
        try:
            driver = Firefox(executable_path = firefoxDriver)
            return driver
        
        except WebDriverException:
            print("Failed to initialize Firefox driver")
        
    return None

def agreeLicence(driver):
    licence = driver.find_element_by_id("qc-cmp2-ui")
    buttonList = licence.find_elements_by_tag_name("button")
    
    for button in buttonList:
        if button.get_attribute("mode") == "primary":
            button.click()
            break
    return

def updateData(driver):
    """
    Met à jour les données du joueur
    """
    driver.find_element_by_id("SummonerRefreshButton").click()
    time.sleep(5)
    return

def showMoreGames(driver):
    """
    Renvoie True si des parties on été charger
    Renvoie False si aucune partie supplémentaires n'a été chargé
    """
    try:
        moreGameButton = WebDriverWait(driver, timeout = 0.5).until(
            lambda d: d.find_element_by_class_name("GameMoreButton"))
        
        moreGameButton.click()
        time.sleep(0.1)
        return True
    except TimeoutException:
        return False

def getGameList(driver):
    gameItemList = driver.find_elements_by_class_name("GameItemList")
    gameList = []
    for game in gameItemList:
        gameList += game.find_elements_by_class_name("GameItemWrap")
    return gameList

def findChampion(name, liList):
    playerStats = None
    for li in liList:
        img = li.find_element_by_tag_name("img")
        if name in img.get_attribute("src"):
            playerStats = li
            break
    return playerStats

def textToInt(txt):
    string = txt.text
    if string == "":
        return 0
    else:
        return int(string.replace(",", ""))

def getGeneralStats(game):
    stats = {}
    stats["type"] = game.find_element_by_class_name("GameType").text
    
    timeStamp = game.find_element_by_class_name("TimeStamp")
    stats["date"] = timeStamp.find_element_by_tag_name("span").get_attribute("title")
    
    stats["win"] = game.find_element_by_class_name("GameResult").text
    stats["duration"] = game.find_element_by_class_name("GameLength").text
    stats["champion"] = game.find_element_by_class_name("ChampionName").text

    kda = game.find_element_by_class_name("KDA")
    kda = kda.find_elements_by_tag_name("span")
    stats["kda"] = [int(kda[0].text), int(kda[1].text), int(kda[2].text)]
    
    csStr = game.find_element_by_class_name("CS").text
    stats["cs"] = int(csStr.split(" ")[0])
    return stats

def getTeamAnalysisData(game, stats):
    try:
        teamData = game.find_element_by_class_name("MatchDetailMatchAnalysis")
    except NoSuchElementException:
        return False
    div = game.find_element_by_class_name("GameSettingInfo")
    im = div.find_element_by_class_name("ChampionImage")
    nim = im.find_element_by_tag_name("img")
    url = nim.get_attribute("src")
    
    champImgName = re.search("[a-zA-Z0-9]+\.png", url).group(0).replace(".png", "")
    #For some champion the name of the image may differ from the champion name
    
    data = teamData.find_elements_by_class_name("MatchAnalysisListItem")
    gold = data[1]
    playerGold = findChampion(champImgName, 
                              gold.find_elements_by_tag_name("li"))

    champDamage = data[2]
    playerChampDamage = findChampion(champImgName, 
                                     champDamage.find_elements_by_tag_name("li"))

    takenDamage = data[4]
    playerTakenDamage = findChampion(champImgName, 
                                     takenDamage.find_elements_by_tag_name("li"))
    
    stats["gold"] = textToInt(playerGold)
    stats["champDamage"] = textToInt(playerChampDamage)
    stats["takenDamage"] = textToInt(playerTakenDamage)
    
    return stats

def showGameDetail(game):
    time.sleep(0.5)
    game.find_element_by_class_name("StatsButton").find_element_by_id("right_match").find_element_by_tag_name("span").click()
    return

def getStats(game):
    """
    Structure du dictionnaire renvoyé par la fonction
        {
           "type" : string, #aram, draft, rank, flex
           "date" : string,
           "win" : string,
           "champion" : string,
           "duration" : string
           "kda" : list [int, int, int],
           "cs" : int,
           "gold" : int,
           "champDamage" : int,
           "takenDamage" : int,
           }
        """
    stats = getGeneralStats(game)
    showGameDetail(game)
    
    print(stats["champion"])
    
    isLoaded = False
    while(not(isLoaded)):
        try:
            game.find_element_by_id("right_match_team").click()
            time.sleep(0.5)
            isLoaded = True
        except NoSuchElementException:
            time.sleep(0.1)
        
    var = None
    while(type(var) != dict):
        #Some elements could not be loaded properly so, wait until they are loaded
        var = getTeamAnalysisData(game, stats)
        time.sleep(0.1)
        
    stats = var
    
    #Close tab where the data is, to have less lag
    game.find_element_by_class_name("StatsButton").click()
    
    return stats

def closeFootagePub(driver):
    try:
        pub = driver.find_element_by_class_name("vm-footer-close")
        pub.click()
    except NoSuchElementException:
        pass
    return

def getPlayerGames(region, playerName, nbOfGames, driver = None):
    if driver == None:
        driver = getDriver(usingFirefox = True)
    
    if driver != None:
        driver.get("https://" + region + ".op.gg/summoner/userName=" + playerName)
        time.sleep(5)
        agreeLicence(driver)
        
        updateData(driver)
        time.sleep(6)
        closeFootagePub(driver)
        
        i = 0
        while(showMoreGames(driver) and i < nbOfGames/10 ): i += 1
        
        gameList = getGameList(driver)
            
        player = []
        for game in gameList:
            player.append(getStats(game))
        return driver, player
    else:
        print("Error, driver object is not instantiated")
        return
    
if __name__ == "__main__":
    
    driver, gameList = getPlayerGames("euw", "android01", 50)
    for game in gameList:
        print(game)
