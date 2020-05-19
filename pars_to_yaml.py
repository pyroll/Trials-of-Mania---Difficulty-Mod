import json
import yaml
import os


def json2yaml():
    with open('yaml files\\json-for-parsing.yaml', 'r') as file:
        jsonYamlData = yaml.load(file, Loader=yaml.FullLoader)
    
    # Work with one key entry at a time (ex. '_01_eb11_01_PartsStatusTable.json')
    for filenameKey in jsonYamlData:
        # Grab type_id from json-for-parsing.yaml
        type_id = jsonYamlData[filenameKey]['type_id']

        fullPath = jsonYamlData[filenameKey]['fullPath']                           

        # edit the file path name so that it points to the .uexp location. The file names for both the 
        # json and uexp are the same except for the leading '_' in the json file and the
        # file extension                
        uexpPath = renameFilenameUexp(filenameKey, fullPath)            

        # Starting offset for common enemies *** This may differ between datatables ***
        offsetIterator = startingOffsetDict[type_id]

        # Open our json file and read it
        with open(fullPath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Iterate through each enemy/entry in the opened json file
        for entry in data:
            # Grab its name and hp values
            enemyName = entry['Value']['Name_29_7A62483740A6D0DF1414CB9963F7CF87']
            enemyHP = entry['Value']['Hp_2_D1FBB5E1450A631F5BB06780E7A9D1EF']                           

            # Check for dummy entry and adjust offsetIterator if needed
            if enemyName == 'dummy':                
                offsetIterator += incrementOffsetDict[type_id]                    
                # Loop back and start next enemy/entry
                continue                                    
            
            # check for duplicate 'enemyName' in 'dictForYaml' to avoid an enemy being overwritten                        
            enemyName = countDuplicates(enemyName, dictForYaml)                
                    
            dictForYaml[enemyName] = {'type_id': type_id, 'filePath': uexpPath, 'offsetLoc': offsetIterator}            

            offsetIterator += incrementOffsetDict[type_id]
        
    # # Writes 'preStats-for-debugging.yaml'
    # processDataForDebugging(data)


def renameFilenameUexp(filenameKey, fullPath):
    # edit the file path name so that it points to the .uexp location. The file names for both the 
    # json and uexp are the same except for the leading '_' in the json file and the
    # file extension                
    uexpSuffix = filenameKey[1:-5] + ".uexp"        
    trimPath = fullPath.replace('JSON Game Files', 'Game Files')
    trimPath = trimPath.replace(filenameKey, "")
    uexpPath = trimPath + uexpSuffix            
    return uexpPath


def countDuplicates(enemyName, dictForYaml):
    dupCounter = 1
    while enemyName in dictForYaml:
        if enemyName[-2] == "_":
            enemyName = enemyName[:-2]
        if enemyName[-3] == "_":
            enemyName = enemyName[:-3]
        enemyName += "_" + str(dupCounter)
        dupCounter += 1                
    return enemyName


def processDataForDebugging():
    with open('yaml files\\json-for-parsing.yaml', 'r') as file:
        jsonYamlData = yaml.load(file, Loader=yaml.FullLoader)
    
    # Work with one key entry at a time (ex. '_01_eb11_01_PartsStatusTable.json')
    for filenameKey in jsonYamlData:
        # Grab type_id from json-for-parsing.yaml
        type_id = jsonYamlData[filenameKey]['type_id']

        fullPath = jsonYamlData[filenameKey]['fullPath']                           

        # edit the file path name so that it points to the .uexp location. The file names for both the 
        # json and uexp are the same except for the leading '_' in the json file and the
        # file extension                
        uexpPath = renameFilenameUexp(filenameKey, fullPath)            

        # Starting offset for common enemies *** This may differ between datatables ***
        offsetIterator = startingOffsetDict[type_id]

        # Open our json file and read it
        with open(fullPath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
        # skip dummy enemy        
        for entry in data:
            enemyName = entry['Value']['Name_29_7A62483740A6D0DF1414CB9963F7CF87']

            if enemyName == 'dummy':
                continue                        

            # --------------------------------------------------------------- #
            enemyHP = entry['Value']['Hp_2_D1FBB5E1450A631F5BB06780E7A9D1EF']
            enemyAtk = entry['Value']["Offense_23_C7833DBF45E6E471939C4CB24F71C6CE"]
            enemyDef = entry['Value']["Defense_11_CEDA3DA940B12870F88BDDB032EED6B7"]
            enemyLuck = entry['Value']["Luck_19_FC9354FC4B582B7003B3748B2304D1E2"]
            enemyDefMag = entry['Value']["DefenseMagic_22_712E9C644CF414B2620BB780F482DDE8"]
            
            # Locate offMag
            for i in entry['Value'].keys():
                # print(i)
                if i.startswith('OffenseMagic'):
                    offMagFinder = i                                        
            enemyOffMag = entry['Value'][offMagFinder]
            # --------------------------------------------------------------- #        
            
            # --------------------------------------------------------------- #
            # Locate exp
            # this and some others are located inside of 'EnemyStatus_...'/'EnemyZParam'
            for i in entry['Value'].keys():            
                if i.startswith('EnemyStatus'):
                    expFinder = i
                elif i.startswith('EnemyZParam'):
                    expFinder = i
            enemyExp = entry['Value'][expFinder]["Exp"]                

            # Locate dropSpp
            for i in entry['Value'][expFinder].keys():            
                if i == 'DropSpp':
                    dropSppFinder = i
            enemyDropSpp = entry['Value'][expFinder][dropSppFinder]

            # Locate KnockOutDropSpp
            for i in entry['Value'][expFinder].keys():            
                if i.startswith('KnockOutDropSpp'):
                    knockoutSppFinder = i
            enemyKnockoutSpp = entry['Value'][expFinder][knockoutSppFinder]

            # Locate LAttackDropSpp
            for i in entry['Value'][expFinder].keys():            
                if i.startswith('LAttackDropSpp'):
                    lAttackSppFinder = i
            enemyLAtkSpp = entry['Value'][expFinder][lAttackSppFinder]

            # Locate ChargeAttackDropSpp
            for i in entry['Value'][expFinder].keys():            
                if i.startswith('ChargeAttackDropSpp'):
                    chargeAttackSppFinder = i
            enemyChAtkSpp = entry['Value'][expFinder][chargeAttackSppFinder]
            # --------------------------------------------------------------- #

            # --------------------------------------------------------------- #        
            enemyLucDrop = entry['Value'][expFinder]["DropLuc"]

            # Locate itemdrops
            if entry['Value'][expFinder]["DropItemProbability"] == []:
                enemyDropProb_0 = None
                enemyDropProb_1 = None
                enemyDropProb_2 = None
                pass
            else:
                enemyDropProb_0 = entry['Value'][expFinder]["DropItemProbability"][0]
                enemyDropProb_1 = entry['Value'][expFinder]["DropItemProbability"][1]
                enemyDropProb_2 = entry['Value'][expFinder]["DropItemProbability"][2]        

            # --------------------------------------------------------------- #
            enemyDownDurable = entry['Value']["DownDurableValue_36_9434D3F24A970695E5621AAECED78C93"]

            # Locate guardDurable
            for i in entry['Value'].keys():            
                if i.startswith('GuardDurableValue'):
                    guardDurFinder = i                                        
            enemyGuardDurable = entry['Value'][guardDurFinder]

            # Locate actionEnableBit
            for i in entry['Value'].keys():            
                if i.startswith('ActionEnableBit'):
                    actEnableFinder = i
            enemyActEnable = entry['Value'][actEnableFinder]
            # --------------------------------------------------------------- #

            # check for duplicate 'enemyName' in 'dictForYaml' to avoid an enemy being overwritten                        
            enemyName = countDuplicates(enemyName, dictForDebug)

            # enemyName = enemyName.decode('utf-8')

            if not enemyDropProb_0 and enemyDropProb_0 != 0:
                dictForDebug[enemyName] = { 'type_id': type_id, 'hp': enemyHP,
                                            'atk': enemyAtk, 'def': enemyDef,
                                            'luck': enemyLuck, 'defMag': enemyDefMag,
                                            'offMag': enemyOffMag, 'exp': enemyExp,
                                            'dropSpp': enemyDropSpp, 'KnockOutDropSpp': enemyKnockoutSpp,
                                            'LAttackDropSpp': enemyLAtkSpp, 'ChargeAttackDropSpp': enemyChAtkSpp,
                                            'DropLuc': enemyLucDrop,
                                            'downDurable': enemyDownDurable, 'guardDurable': enemyGuardDurable,
                                            'actionEnable': enemyActEnable, 'jsonPath': fullPath}
            else:
                dictForDebug[enemyName] = { 'type_id': type_id, 'hp': enemyHP,
                                            'atk': enemyAtk, 'def': enemyDef,
                                            'luck': enemyLuck, 'defMag': enemyDefMag,
                                            'offMag': enemyOffMag, 'exp': enemyExp,
                                            'dropSpp': enemyDropSpp, 'KnockOutDropSpp': enemyKnockoutSpp,
                                            'LAttackDropSpp': enemyLAtkSpp, 'ChargeAttackDropSpp': enemyChAtkSpp,
                                            'DropLuc': enemyLucDrop, 'itemDrop1': enemyDropProb_0,
                                            'itemDrop2': enemyDropProb_1, 'itemDrop3': enemyDropProb_2,
                                            'downDurable': enemyDownDurable, 'guardDurable': enemyGuardDurable,
                                            'actionEnable': enemyActEnable, 'jsonPath': fullPath}            


# enemyCategories = ['common', 'boss', 'shinju', 'parts']

# We want to store the name, HP, and offset location for each enemy in a yaml file
dictForYaml = {}

dictForDebug = {}

startingOffsetDict = {
            'common': 111,
            'boss': 140,   
            'shinju': 140,
            'parts': 111
}

incrementOffsetDict = {
            'common': 1579,
            'boss': 1624,            
            'shinju': 1624,
            'parts': 1579
}

json2yaml()

# write new yaml file
with open('yaml files\\parsed_ene_data.yaml', 'w', encoding='utf-8') as file:    
    yaml.safe_dump(dictForYaml, file, allow_unicode=True)


processDataForDebugging()

with open('yaml files\\preStats-for-debugging.yaml', 'w', encoding='utf-8') as file:
    yaml.safe_dump(dictForDebug, file, allow_unicode=True)
