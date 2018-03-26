import json
import urllib.request
import string

class Character():
    def __init__(self):
        self.battleRank = 0
        self.creationDate = "00:00 UTC"
        self.playTime = 0
        self.name = ""
        self.faction = ""
        self.charID = 0
        
        self.currentCerts = 0
        self.spentCerts = 0
        self.percentToNextCert = 0
        self.giftedCerts = 0
        self.earnedCerts = 0
       
        
        self.remainingRibbons = 0
        self.lastLogin = "DD/MM/YYYY - 00:00 UTC"
        self.lastSaved = "DD/MM/YYYY - 00:00 UTC"

        self.kills = 0
        self.deaths = 0
        self.KD = 0.0
        self.accuracy = 0.0

        self.server = "Gemini"
        

class Outfit():
    def __init__(self):
        self.tag = "HIVE"
        self.ID = 0
        self.creationDate = "xxx"
        self.memberCount = 2
        self.name = "The HIVE"
        self.leaderName = "Bob"
        
        
#[RAW] BR, all cert values, ribbons, percent to next, ID, name
#[DATE] creationDate ,lastLogin, lastSaved 
#[CONVERTED] factionID -> String, PlayTime in Mins -> Hours
        
def getData(character=""):
    #searchedCharacter = getCharacterName()
    searchedCharacter = character.lower()
    apiData,validResponse = apiCharacterQuery(searchedCharacter)
    if validResponse == True:
        print("Character Found")
        playerCharacter = createCharacterObject(apiData)
    elif validResponse == False:
        print("Valid API data was not returned, please try again")
        playerCharacter = None
    else:
        print("You messed up the API function")
        playerCharacter = None
    
    return playerCharacter


def returnCharacter(character=""):
    char = getData(character)
    if char == None:
        charSummary = "Invalid Character"
        char = Character()
    else:
        charSummary = ("Name: " + char.name + "\n" +
          "Server: " + char.server + "\n" +
          "Faction: " + char.faction + "\n" +
          "Battle Rank: " + str(char.battleRank) + "\n" +
          "K/D Ratio: " + str(char.KD) + "\n" + 
          "Time Played: " + str(char.playTime) + " Hours" + "\n")
        print(char.kills)
    return charSummary, char

def returnStat(character,stat):
    char = getData(character)
    if char == None:
        requestedStat = "Invalid Character"
        char = Character()
    else:
        if stat == "Name":
            requestedStat = char.name
        elif stat== "Faction":
            requestStat = "Faction: " + str(char.faction)
        elif stat == "CreationDate":
            requestedStat = "Creation Date: " + str(char.creationDate)
        elif stat == "LastSave":
            requestedStat = "Character Last Saved: " + str(char.lastSaved)
        elif stat == "LastLogin":
            requestedStat = "Last Login: " + str(char.lastLogin)
        elif stat == "PercentToCert":
            requestedStat = str(round(char.percentToNextCert)) + "% to next cert"
        elif stat == "PlayTime":
            requestedStat = "Playtime: " + str(char.playTime) + " Hours"
        elif stat == "EarnedCerts":
            requestedStat = str(char.earnedCerts) + " Certs Earned"
        elif stat == "GiftedCerts":
            requestedStat = str(char.giftedCerts) + " Passive Certs Gained"
        elif stat == "CurrentCerts":
            requestedStat = str(char.currentCerts) + " Certs Available"
        elif stat == "SpentCerts":
            requestedStat = str(char.spentCerts) + " Certs Spent"
        elif stat == "BattleRank":
            requestedStat = "Battle Rank: " + str(char.battleRank)
        elif stat == "DailyRibbons":
            requestedStat = str(char.remainingRibbons) + " Ribbons Remaining Today"
        elif stat == "CharacterID":
            requestedStat = "Character ID: " + str(char.charID)
        elif stat == "Kills":
            requestedStat = "Kills: " + str(char.kills)
        elif stat == "Deaths":
            requestedStat = "Deaths: " + str(char.deaths)
        elif stat == "KD":
            requestedStat = "K/D Ratio: " + str(char.KD)
        elif stat == "Accuracy":
            requestedStat = "Accuracy: " + str(char.accuracy) + "%"
        else:
            requestedStat = "Invalid Stat"
            print(stat)
    return requestedStat, char
        
def getCharacterName(): #Asks the user for a character name
    userCharacter = str(input("What character do you want to look up: ")).lower()
    return userCharacter

def apiCharacterQuery(searchString,queryParameter="name.first_lower"): #Takes a method of searching the PS2 API and the string to search. 
    #General Data for Most Uses
    validResponse = False
    urlBase = urllib.request.urlopen("http://census.daybreakgames.com/s:PlanetsideBattles/get/ps2:v2/character/?" + queryParameter + "=" + searchString + "&c:resolve=world,stat_history,weapon_stat")
    str_responseBase = urlBase.read().decode('utf-8')
    objBase = json.loads(str_responseBase)

    #Weapon Data for Acc Calculations
    #urlWeapon = urllib.request.urlopen("http://census.daybreakgames.com/s:PlanetsideBattles/get/ps2:v2/character/?" + queryParameter + "=" + searchString + "&c:resolve=weapon_stat")
    #str_responseWeapon = urlWeapon.read().decode('utf-8')
    #objWeapon = json.loads(str_responseWeapon)
    responseNum = int(objBase['returned'])
    if responseNum > 0:
        validResponse = True
    else:
        validResponse = False
        print("No Results Returned.")
    
    return objBase,validResponse #Returns the JSON response

def resolveFaction(factionID):
    if factionID == 1:
        faction = "Vanu Sovereignty"        
    elif factionID == 2:
        faction = "New Conglomerate"
    elif factionID == 3:
        faction = "Terran Republic"
    else:
        faction = "Invalid Faction"
        print("Invalid Faction")
    return faction

def resolveServer(serverID):
    serverID = int(serverID)
    if serverID == 1:
        server = "Connery"
    elif serverID == 10:
        server = "Miller"
    elif serverID == 13:
        server = "Cobalt"
    elif serverID == 17:
        server = "Emerald"
    elif serverID == 19:
        server = "Jaeger"
    elif serverID == 25:
        server == "Briggs"
    else:
        server = None
    return server

def calculateAccuracy(charObject):
    weaponList = charObject['stats']['weapon_stat']
    #print(charObject['stats'])
    hitCount = 0
    shotCount = 0
    testVar = 0
    #invalidWep = ['1044', '1045', '1084', '1095', '1096', '16032', '16033', '17000', '17001', '17004', '17012', '17013', '17016', '17024', '17025', '17030', '19', '2500', '2510', '286', '35002', '35003', '35004', '429', '432', '4445',
                  #'4446', '4447', '44705', '50051', '501', '50560', '50561', '5494', '5500', '5501', '5502', '551', '5512', '5513', '5514', '5515', '554', '650', '6550', '6553', '6556', '6559', '700', '703', '7213', '75083', '7519',
                  #'7520', '7525', '7540', '75490', '7755', '800626', '801969', '802106', '802514', '86', '882', '1', '1082', '1083', '1097', '13', '15000', '15001', '15004', '15012', '15013', '15016', '15024', '15025', '15030', '16000',
                  #'16001', '16004', '16012', '16013', '16016', '16024', '16025', '16026', '16028', '16029', '16030', '16031', '1849', '2308', '2309', '2310', '2318', '2501', '2502', '2508', '2509', '2511', '2512', '2659', '266', '271',
                  #'285', '33002', '33003', '33004', '34002', '34003', '34004', '44505', '44605', '4745', '4746', '4747', '502', '503', '5050', '5051', '5052', '50562', '5220', '5442', '5443', '5495', '5496', '5504', '5506', '5507',
                  #'5509', '5511', '5516', '5518', '5519', '552', '5520', '5522', '5523', '553', '555', '556', '6552', '6554', '6555', '6563', '701', '702', '704', '705', '7102', '7127', '7172', '7192', '7390', '7505', '7506', '7507',
                  #'7512', '7513', '7518', '7528', '7533', '800623', '800625', '802300', '802315', '802316', '802322', '802517', '802518', '802584', '84', '85', '880', '881', '129', '267', '5517', '6551', '101', '1254', '1255', '1278',
                  #'154', '1627', '1628', '1629', '1630', '466', '481', '482', '483', '484', '485', '6010', '7', '71565', '75289', '7611', '802512', '124', '1252', '1253', '1274', '1626', '377', '44506', '472', '5503', '75288', '884',
                  #'93', '125', '126', '1275', '1276', '1277', '153', '2657', '309', '376', '45', '46', '47', '471', '500', '5218', '71563', '71564', '75285', '75286', '75287', '94', '95', '5441', '800627', '801970', '802299', '802317',
                  #'5521', '2658', '6557', '6558', '800624', '5219', '5505', '5508', '5510', '6561', '6564', '2317', '802025', '802301', '1261', '1273', '1612', '802515', '1260', '6011', '1268', '7610', '486', '1256', '6012', '1257',
                  #'6562', '1258', '1259', '6560', '1611', '478', '487', '802516', '100', '1608', '1609', '1610', '6050', '1272', '802302', '1263', '1262', '1264', '1617', '1619', '1621', '1620', '7609', '1618', '99', '802903', '883',
                  #'802902', '76358', '474', '473', '475', '1267', '476', '1265', '1266', '1269', '477', '479', '480', '1270', '1271', '727', '557', '724', '730']
    for item in weaponList:
        if item['stat_name'] == "weapon_fire_count" :
            shotCount = shotCount + int(item['value'])
        elif item['stat_name'] == "weapon_hit_count" :
            hitCount = hitCount + int(item['value'])
        else:
            pass
        testVar += 1
        if testVar == 100:
            print(item['stat_name'])
    
    accuracy = round(100*(float(hitCount)/shotCount),2)
    return accuracy
        
def createCharacterObject(apiData):
    characterObject = Character()
    charList = apiData["character_list"]
    userChar = charList[0]
    ####
    characterObject.battleRank = int(userChar['battle_rank']['value'])
    characterObject.faction = resolveFaction(int(userChar['faction_id']))
    characterObject.creationDate = userChar['times']['creation_date']
    characterObject.currentCerts = int(userChar['certs']['available_points'])
    characterObject.spentCerts = int(userChar['certs']['spent_points'])
    characterObject.playTime = round(int(userChar['times']['minutes_played'])/60)
    characterObject.name = userChar['name']['first']
    characterObject.percentToNextCert = float(userChar['certs']['percent_to_next'])
    characterObject.giftedCerts = int(userChar['certs']['gifted_points'])
    characterObject.remainingRibbons = int(userChar['daily_ribbon']['count'])
    characterObject.lastLogin = userChar['times']['last_login_date']
    characterObject.lastSaved = userChar['times']['last_save_date']
    characterObject.charID = userChar['character_id']
    characterObject.earnedCerts = userChar['certs']['earned_points']
    characterObject.kills = int(userChar['stats']['stat_history'][5]['all_time'])
    characterObject.deaths = int(userChar['stats']['stat_history'][2]['all_time'])
    characterObject.KD = round(float(characterObject.kills)/float(characterObject.deaths),2)
    characterObject.server = resolveServer(userChar['world_id'])
    characterObject.accuracy = calculateAccuracy(userChar)
    return characterObject

def characterSites(charName):
    #Take the name
    goodName = False
    daLink = "stats.dasanfall.com/ps2/player/AtherumVS"
    fisuLink = "ps2.fisu.pw/player/?name=AtherumVS"
    planetstatsLink = "www.planetstats.net/atherumvs"
    try:
        charName = str(charName)
        goodName = True
    except ValueError:
        goodName = False
    #create URLs for various sites
    daLink = "stats.dasanfall.com/ps2/player/" + charName
    fisuLink = "ps2.fisu.pw/player/?name=" + charName
    planetstatsLink = "www.planetstats.net/" + charName.lower()
    #return them
    return goodName, daLink, fisuLink, planetstatsLink

def getOutfitData(tag):
    urlBase = urllib.request.urlopen("http://census.daybreakgames.com/s:PlanetsideBattles/get/ps2:v2/outfit/?alias_lower=" + tag.lower() + "&c:resolve=leader(name,type.faction)")
    str_responseBase = urlBase.read().decode('utf-8')
    objBase = json.loads(str_responseBase)
    outfitStats = objBase['outfit_list'][0]
    outfit = Outfit()
    outfit.ID = outfitStats['outfit_id']
    outfit.name = outfitStats['name']
    outfit.tag = outfitStats['alias']
    outfit.memberCount = outfitStats['member_count']
    outfit.creationDate = outfitStats['time_created_date']
    outfit.leaderName = outfitStats['leader']['name']['first']
    print(outfit.tag)
    return outfit

def outfitSummary(tag):
    outfit = getOutfitData(tag)
    summary = ("[" + outfit.tag + "] " + outfit.name + "\n" +
               "Leader: " + outfit.leaderName + "\n" +
               "Created: " + outfit.creationDate + "\n" +
                "Members: " + outfit.memberCount + "\n")
    return summary
