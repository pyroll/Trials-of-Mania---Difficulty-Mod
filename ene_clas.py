import os
import yaml

# TODO do we want to be able to update each class instance so we can check what its new value is?
class Enemy:    
    def __init__(self, enemyType, file_path, hpOffset):
        self.enemyType = enemyType        
        self.fileLocation = file_path        
        self.attrOffsetDict = {}             
        # self.outPath = determineOutPath(enemyType, file_path)

        # Append to appropriate category        
        enemyCategories[enemyType].append(self)

        # Offset locations for each stat we want to edit      
        # hpOffset is used as the base offset to calculate the other offsets   
        for attr, offset in loadedOffsets[enemyType].items():
            self.attrOffsetDict[attr] = hpOffset + offset


def editHexAll(enemyType):
    # Starting directory for file iterating
    # TODO way to prevent errors when rootdir of one enemyType contains the rootdir of a subsequent one
    rootdir = rootDirDict[enemyType]

    # Get full path of file to use
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # This will concatenate the 'head' and 'tail' to form the full file path
            fullPath = os.path.join(subdir, file)
            
            # Avoid working on parts and shinju files while enemyType is 'boss' \
            if enemyType == 'boss' and file != 'BossStatusTable.uexp':
                continue

            with open(fullPath, 'rb') as f:
                byteData = f.read()
        
            # Get data into an array that is mutable
            mutableBytes = bytearray(byteData)

            for enemy in enemyCategories[enemyType]:                
                # Check each Enemy's fileLocation attr to see if it matches the current fullPath
                if enemy.fileLocation == fullPath:
                    for attr, offset in enemy.attrOffsetDict.items():
                        
                        # Original slice of four bytes in data that we will edit
                        fourBytesToEdit = byteData[offset:(offset + 4)]                    

                        # Convert those four bytes to an integer
                        numFromBytes = int.from_bytes(fourBytesToEdit, byteorder='little', signed=True)                    

                        newStatValue = round(numFromBytes * multipliersDict[enemyType][attr])
                        
                        if newStatValue > 2147483647:
                            newStatValue = 2147483647                 

                        # new Stat value to 4 byte string
                        bytesToInsert = newStatValue.to_bytes(4, byteorder='little', signed=True)                    

                        # Insert new byte slice into mutable byte array
                        mutableBytes[offset:(offset + 4)] = bytesToInsert                                            
                       
            with open(determineOutPath(enemyType, file), 'wb') as f:
                f.write(mutableBytes)                    


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


# We need to check that the directories needed for output exist,
# if they do not exist, we will create them
def makeDirectories():
    with open("required-directories.yaml", 'r') as file:
        dirs = yaml.load(file, Loader=yaml.FullLoader)
    
    head = dirs['base']
    # print("base of directories is: " + head)
    if not os.path.exists(head):        
        # print("and so it is created")
        os.makedirs(head)
        
    for enemy_type in ['common', 'boss', 'parts']:
        for key, ene_dir in dirs[enemy_type].items():
            path = head + "\\" + ene_dir
            if not os.path.exists(path):
                os.makedirs(path)
    
    head = head + "\\" + dirs['shinju']['base']
    dirs['shinju'].pop('base') # remove 'base' key as its purpose is different to other members in dir['shinju']
    for key, val in dirs['shinju'].items():
        path = head + "\\" + val
        if not os.path.exists(path):
            os.makedirs(path)


def createEnemyInstances():
    eneDataDir = 'parsed_ene_data'    
    for root, dirs, files in os.walk(eneDataDir):
        for file in files:
            # This will concatenate the 'head' and 'tail' to form the full file path
            fullPath = os.path.join(root, file)            

            with open(fullPath, 'r') as f:
                yamlData = yaml.load(f, Loader=yaml.FullLoader)
            
            for enemyName, info in yamlData.items():
                filePath = info['filePath']
                offsetLoc = info['offsetLoc']
                print(offsetLoc)
                enemyType = info['type_id']

                if enemyType[:7] == "shin_eb":
                    enemyType = 'shinju'

                Enemy(enemyType, filePath, offsetLoc)

# List of all instance lists which will include common enemies, bosses, boss limbs, etc.
enemyCategories = {"common": [], 
                   "boss"  : [],
                   "shinju": [],
                   "parts" : []}

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

with open("offsets-config.yaml", 'r') as file:
    loadedOffsets = yaml.load(file, Loader=yaml.FullLoader)
    
with open('multipliers-config.yaml', 'r') as file:
    multipliersDict = yaml.load(file, Loader=yaml.FullLoader)

makeDirectories()
createEnemyInstances()

for enemyType in ['common', 'boss', 'shinju', 'parts']:
    editHexAll(enemyType)  


print("Please check that the directory 'Custom_TofMania - 0.3.2_P' has new files created.\n" \
        "If the files existed before running this script, they should be updated now.\n")

closeVar = input("Press 'enter' to exit the console.")
closeVar = None
