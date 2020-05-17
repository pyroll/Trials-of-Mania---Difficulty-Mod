import yaml
import struct

# Temporarily replacing multipliers-config.yaml with test-configs
with open("test-config.yaml", 'r') as file:
    multipliersDict = yaml.load(file, Loader=yaml.FullLoader)
# with open('yaml files\\multipliers-config.yaml', 'r') as file:
#     multipliersDict = yaml.load(file, Loader=yaml.FullLoader)

# Testing 'testing-names.yaml'; rename when done
with open("testing-names.yaml", 'r') as file:
    namesGroups = yaml.load(file, Loader=yaml.FullLoader)

enemyType = 'parts'
enemyName = 'Altar_8'
attr = 'itemDrop3'

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
# Check for specific overrides
        elif enemyName in multipliersDict['specific']:
            if attr in multipliersDict['specific'][enemyName]:
                # This replaced the old 'multipliersDict[enemyType][attr]' below
                ourSpecialMultiplier = multipliersDict['specific'][enemyName][attr]
            elif multipliersDict[enemyType] != None:
                if attr in multipliersDict[enemyType]:
                    ourSpecialMultiplier = multipliersDict[enemyType][attr]
                else:
                    ourSpecialMultiplier = multipliersDict['general'][attr]        

print(ourSpecialMultiplier)