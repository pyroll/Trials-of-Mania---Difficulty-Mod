import json
import yaml
import os


# TODO directories outside of git clone are being used for some reason?
def json2yaml(enemyType):
    # We want to store the name, HP, and offset location for each enemy in a yaml file
    dictForYaml = {}
    
    # Get full path of json file to read from
    for root, dirs, files in os.walk(jsonDir[enemyType]):        
        for file in files:            
            
            # Add code to skip the subdirs in ShinjuStatusTableList in enemyType is 'Shinju'
            if (enemyType == 'shinju' and 'PartsStatusTable' in file) or (enemyType == 'shinju' and 'PartsTable' in file):
                continue
            
            fullPath = os.path.join(root, file)                
            
            with open(fullPath, 'r') as f:
                data = json.load(f)

            # edit the file path name so that it points to the .uexp location. The file names for both the 
            # json and uexp are the same except for the leading '_' in the json file and the
            # file extension
            varSuffix = file[1:-5]
            uexpSuffix = file[1:-5] + ".uexp"
            
            # make variable for path to uexp
            uexpPath = uexpOutputDict[enemyType] + uexpSuffix

            # Starting offset for common enemies *** This may differ between datatables ***
            offsetIterator = startingOffsetDict[enemyType]

            # TODO add every stat we want to potentially edit and add it to output file
            # Iterate through each enemy/entry in the read json file
            for entry in data:        
                enemyName = entry['Value']['Name_29_7A62483740A6D0DF1414CB9963F7CF87']
                enemyHP = entry['Value']['Hp_2_D1FBB5E1450A631F5BB06780E7A9D1EF']                           

                # Check for dummy entry and adjust offsetIterator if needed
                if enemyName == 'dummy':                
                    offsetIterator += incrementOffsetDict[enemyType]                    
                    continue                                    
                
                # check for duplicate 'enemyName' in 'dictForYaml' to avoid an enemy being overwritten                        
                dupCounter = 1
                while enemyName in dictForYaml:
                    if enemyName[-2] == "_":
                        enemyName = enemyName[:-2]
                    if enemyName[-3] == "_":
                        enemyName = enemyName[:-3]
                    enemyName += "_" + str(dupCounter)
                    dupCounter += 1                
                        
                dictForYaml[enemyName] = {'type_id': enemyType, 'filePath': uexpPath, 'offsetLoc': offsetIterator}            

                offsetIterator += incrementOffsetDict[enemyType]


    # write new yaml file
    outputPath = 'parsed_ene_data\\' + enemyType + "_data.yaml"
    # r'Trials-of-Mania---Difficulty-Mod\test_data.yaml'
    
    with open(outputPath, 'w') as file:
        yaml.dump(dictForYaml, file)


# dict that holds all the directories with json files to read
jsonDir = {
            'common': r'Game Files\Enemy\JSON for viewing\Orig',
            'boss': r'Game Files\Boss\Orig\JSON for viewing\Charadata',
            'shinju': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList',
            'shin_eb11': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb11_Parts',
            'shin_eb12': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb12_Parts',
            'shin_eb13': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb13_Parts',
            'shin_eb14': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb14_Parts',
            'shin_eb15': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb15_Parts',
            'shin_eb16': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb16_Parts',
            'shin_eb17': r'Game Files\Boss\Orig\JSON for viewing\ShinjuStatusTableList\eb17_Parts',
            'parts': r'Game Files\Boss\Orig\JSON for viewing\Parts'
            }

# the actual file name with the uexp suffix is created in the function, so just add 
# the preceding directory structure
# *** Important to add trailing backslash; raw strings are funky when they end with a single '\'
uexpOutputDict = {
            'common': 'Game Files\\uexp files\\Orig\\',
            'boss': 'Game Files\\Boss\\Orig\\uexp files\\Charadata\\',
            'shinju': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\',
            'shin_eb11': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb11_Parts\\',
            'shin_eb12': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb12_Parts\\',
            'shin_eb13': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb13_Parts\\',
            'shin_eb14': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb14_Parts\\',
            'shin_eb15': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb15_Parts\\',
            'shin_eb16': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb16_Parts\\',
            'shin_eb17': 'Game Files\\Boss\\Orig\\uexp files\\ShinjuStatusTableList\\eb17_Parts\\',
            'parts': 'Game Files\\Boss\\Orig\\uexp files\\Parts\\'
            }

startingOffsetDict = {
            'common': 111,
            'boss': 140,            
            'shinju': 140,
            'shin_eb11': 111,
            'shin_eb12': 111,
            'shin_eb13': 111,
            'shin_eb14': 111,
            'shin_eb15': 111,
            'shin_eb16': 111,
            'shin_eb17': 111,
            'parts': 111
}

incrementOffsetDict = {
            'common': 1579,
            'boss': 1624,            
            'shinju': 1624,
            'shin_eb11': 1579,
            'shin_eb12': 1579,
            'shin_eb13': 1579,
            'shin_eb14': 1579,
            'shin_eb15': 1579,
            'shin_eb16': 1579,
            'shin_eb17': 1579,
            'parts': 1579
}

# Run function for each enemy type
for enemyType in ['common', 'boss', 'shinju', 'shin_eb11', 'shin_eb12', 'shin_eb13', 'shin_eb14',
                     'shin_eb15', 'shin_eb16', 'shin_eb17', 'parts']:
    json2yaml(enemyType)