import os
import yaml
import struct
from collections import defaultdict


class Enemy:
    def __init__(self, enemyName, enemyType, file_path, hpOffset):
        self.enemyName = enemyName      
        self.enemyType = enemyType        
        self.fileLocation = file_path        
        self.attrOffsetDict = {}               

        enemiesByFile[file_path].append(self) 
        
        # Offset locations for each stat we want to edit      
        # hpOffset is used as the base offset to calculate the other offsets   
        for attr, offset in loadedOffsets[enemyType].items():
            self.attrOffsetDict[attr] = hpOffset + offset


# TODO begin testing edits with test-config.yaml; use that one when finished
def editHexAll():
    with open("yaml files\\files-to-edit.yaml", 'r') as file:
        files = yaml.load(file, Loader=yaml.FullLoader)

    # needed for debugEdits()
    with open("yaml files\\preStats-for-debugging.yaml", 'r') as file:
        preStatsData = yaml.load(file, Loader=yaml.FullLoader)    
    
    for file in files:                
        fullPath = files[file]['fullPath']
        outPath = files[file]['outPath']    
           
        with open(fullPath, 'rb') as f:
            byteData = f.read()

        mutableBytes = bytearray(byteData) 

        for enemy in enemiesByFile[fullPath]:                                    

            for attr, offset in enemy.attrOffsetDict.items():
                editBytes(mutableBytes, enemy, attr, offset, preStatsData)                                                   
                                               
        with open(outPath, 'wb') as f:
            f.write(mutableBytes)              


# TODO Currently testing with test-config.yaml
def editBytes(mutableBytes, enemy, attr, offset, preStatsData):    
    enemyType = enemy.enemyType
    enemyName = enemy.enemyName    

    # use specific name grouping
    if multipliersDict['specific'] == None:
        if multipliersDict[enemyType] != None:
            if attr in multipliersDict[enemyType]:
                ourSpecialMultiplier = multipliersDict[enemyType][attr]
            else:
                ourSpecialMultiplier = multipliersDict['general'][attr]
    else:
        for i in multipliersDict['specific']:
            if enemyName in namesGroups[i]:
                # groupName = namesGroups[i]
                if attr in multipliersDict['specific'][i]:
                    ourSpecialMultiplier = multipliersDict['specific'][i][attr]
                else:
                    pass
    # Check for specific overrides
            if enemyName in multipliersDict['specific']:
                if attr in multipliersDict['specific'][enemyName]:
                    # This replaced the old 'multipliersDict[enemyType][attr]' below
                    ourSpecialMultiplier = multipliersDict['specific'][enemyName][attr]
            elif multipliersDict[enemyType] != None:
                if attr in multipliersDict[enemyType]:
                    ourSpecialMultiplier = multipliersDict[enemyType][attr]
                else:
                    ourSpecialMultiplier = multipliersDict['general'][attr]
            else:
                ourSpecialMultiplier = multipliersDict['general'][attr] 

    # Original slice of four bytes in data that we will edit
    fourBytesToEdit = mutableBytes[offset:(offset + 4)]                    

    # Use conditional to determine if value is a float or an integer
    if attr == 'guardDurable' or attr == 'downDurable':
        numFromBytes = struct.unpack('<f', fourBytesToEdit)

        # multipliersDict comes from our test-config.yaml file
        newStatValue = numFromBytes[0] * ourSpecialMultiplier
        newStatValue = round(newStatValue, 1)

        newStatValue = min(newStatValue, 2147483647)
    else:  # handle it as an integer
        # Convert those four bytes to an integer
        numFromBytes = int.from_bytes(fourBytesToEdit, byteorder='little', signed=True)                    

        newStatValue = round(numFromBytes * ourSpecialMultiplier)
                                
        newStatValue = min(newStatValue, 2147483647)

    # Debug/Assert that value is what it's supposed to be
    debugEdits(enemyName, enemyType, attr, newStatValue, preStatsData, ourSpecialMultiplier)                 

    # new Stat value to 4 byte string
    if type(newStatValue) == float:
        bytesToInsert = bytearray(struct.pack('f', newStatValue))
        assert len(bytesToInsert) == 4
    else:
        bytesToInsert = newStatValue.to_bytes(4, byteorder='little', signed=True)                    
        assert len(bytesToInsert) == 4

    # Insert new byte slice into mutable byte array
    mutableBytes[offset:(offset + 4)] = bytesToInsert


def debugEdits(enemyName, enemyType, attr, newStatValue, preStatsData, ourSpecialMultiplier):    
    preEditEnemy = preStatsData[enemyName]
    preStat = preEditEnemy[attr]
    currentMultiplier = ourSpecialMultiplier

    if type(preStat) == float:
        roundedNewStatValue = round(newStatValue, 1)
        assert preStat * currentMultiplier == roundedNewStatValue
    else:
        assert round(preStat * currentMultiplier) == newStatValue


# We need to check that the directories needed for output exist,
# if they do not exist, we will create them
def makeDirectories():
    with open("yaml files\\required-directories.yaml", 'r') as file:
        dirs = yaml.load(file, Loader=yaml.FullLoader)
    
    head = dirs['base']
    if not os.path.exists(head):        
        os.makedirs(head)
        
    for tail in dirs['tails']:        
            fullPath = head + "\\" + tail
            if not os.path.exists(fullPath):
                os.makedirs(fullPath)
    

def createEnemyInstances():
    readiedData = 'yaml files\\parsed_ene_data.yaml'            

    with open(readiedData, 'r') as f:
        yamlData = yaml.load(f, Loader=yaml.FullLoader)
    
    for enemyName, info in yamlData.items():        
        filePath = info['filePath']
        offsetLoc = info['offsetLoc']
        enemyType = info['type_id']                                              

        Enemy(enemyName, enemyType, filePath, offsetLoc)


enemiesByFile = defaultdict(list)

# rootDirDict = {"common": r'Game Files\uexp files\Orig', 
#                "boss"  : r'Game Files\Boss\Orig\uexp files',
#                "shinju": r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList',
#                "parts" : r'Game Files\Boss\Orig\uexp files\Parts'}

# paths we want the edited files to output to for UnrealPak.exe
# finDirPath_BP = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\BP\\Enemy\\Zako\\Data\\'
# finDirPath_Data = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\'
# finDirPath_Boss = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\'
# finDirPath_shinju = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\ShinjuStatusTableList\\'
# finDirPath_parts = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\Parts\\'

with open("yaml files\\offsets-config.yaml", 'r') as file:
    loadedOffsets = yaml.load(file, Loader=yaml.FullLoader)

with open("multipliers-config.yaml", 'r') as file:
    multipliersDict = yaml.load(file, Loader=yaml.FullLoader)

with open("yaml files\\name-groups.yaml", 'r') as file:
    namesGroups = yaml.load(file, Loader=yaml.FullLoader)


makeDirectories()
createEnemyInstances()

editHexAll()  


print("Please check that the directory 'Custom_TofMania - 0.5_P' has new files created.\n" \
        "If the files existed before running this script, they should be updated now.\n")

closeVar = input("Press 'enter' to exit the console.")
