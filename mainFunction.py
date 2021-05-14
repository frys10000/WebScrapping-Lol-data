# -*- coding: utf-8 -*-
"""
Created on Sun May  9 16:50:12 2021

@author: android01
"""

import urllib.request as ur
import bs4

region = {"BR": "br",
          "EUNE": "eune",
          "EUW": "euw",
          "JP": "jp",
          "KR": "kr",
          "LAN": "lan",
          "LAS": "las",
          "NA": "na",
          "OCE": "oce",
          "RU": "ru",
          "TR": "tr"}

def getEncoding(headers):
    """
    Parameters
    ----------
    headers : List of tuple
        contain all 

    Renvoie, l'encodage d'une page html, à partir des headers
    
    """
    encoding = ""
    
    for header in headers:
        for data in header:
            if "charset=" in data:
                encoding = data.split("=")[1].replace(";", "")
                break
    return encoding

def decodedUrl(url):
    #Used to say that the request comme from Mozilla not Python
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    html = ur.urlopen(ur.Request(url, headers = headers))
    
    headers = html.getheaders()
    
    html = html.read()
        
    html = html.decode(encoding = getEncoding(headers))    
    return html

def getBestPlayer(zone):
    url = "https://www.leagueofgraphs.com/fr/rankings/summoners/"
    url = url + region[zone]

    htmlSoup = bs4.BeautifulSoup(decodedUrl(url), "html.parser")
    bestPlayers = htmlSoup.find_all("span", {'class' : 'name'})
    playerList = []
    
    for line in bestPlayers:
            playerList.append(line.get_text())
    
    return playerList
