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
        with open(fullPath, 'r') as f:
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


# enemyCategories = ['common', 'boss', 'shinju', 'parts']

# We want to store the name, HP, and offset location for each enemy in a yaml file
dictForYaml = {}

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
outputPath = 'yaml files\\parsed_ene_data.yaml'

with open(outputPath, 'w') as file:
    documents = yaml.dump(dictForYaml, file)
