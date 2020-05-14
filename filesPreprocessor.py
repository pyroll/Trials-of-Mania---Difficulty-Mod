import os
import yaml
from collections import defaultdict


def determineOutPath(enemyType, file):
    if enemyType == 'common' and (file == 'EnemyStatusTable.uexp' or file == 'EnemyStatusMaxTable.uexp'):
        return finDirPath_Data + file
    elif enemyType == 'common':
        return finDirPath_BP + file
    
    if file == 'BossStatusTable.uexp':        
        return finDirPath_Boss + file 

    if enemyType == 'parts':
        return finDirPath_parts + file

    if 'CustomStatusTable.uexp' in file:
        return finDirPath_shinju + file
    
    # At this point, the only files that remain are ones of the form: 
    # 01_eb11_01_PartsStatusTable.uexp
    if file[3:5] != 'eb':
        print(file)
        print(enemyType)        
        raise Exception("Unexpected file in determining outpath")

    return finDirPath_shinju + "\\eb" + file[5:7] + "_Parts\\" + file


def preprocessFiles(enemyType):
    rootdir = rootDirDict[enemyType]    

    # Get full path of file to use
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if enemyType == 'boss' and file != 'BossStatusTable.uexp':
                continue
            
            # This will concatenate the 'head' and 'tail' to form the full file path
            fullPath = os.path.join(subdir, file)

            outPath = determineOutPath(enemyType, file)

            filesToEditDict[file]["fullPath"] = fullPath
            filesToEditDict[file]["outPath"] = outPath        


rootDirDict = {"common": r'Game Files\uexp files\Orig', 
               "boss"  : r'Game Files\Boss\Orig\uexp files',
               "shinju": r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList',
               "parts" : r'Game Files\Boss\Orig\uexp files\Parts'}

# paths we want the edited files to output to for UnrealPak.exe
finDirPath_BP = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\BP\\Enemy\\Zako\\Data\\'
finDirPath_Data = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\'
finDirPath_Boss = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\'
finDirPath_shinju = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\ShinjuStatusTableList\\'
finDirPath_parts = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\Parts\\'

filesToEditDict = defaultdict(dict)

for enemyType in ['common', 'boss', 'shinju', 'parts']:
    preprocessFiles(enemyType)  

filesToEditDict = dict(filesToEditDict)

with open("files-to-edit.yaml", 'w') as file:
    yaml.dump(filesToEditDict, file)