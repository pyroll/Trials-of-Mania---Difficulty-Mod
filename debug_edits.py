import json
import yaml


def editHexAll():
    with open("yaml files\\files-to-edit.yaml", 'r') as file:
        files = yaml.load(file, Loader=yaml.FullLoader)       
    
    for file in files:                
        fullPath = files[file]['fullPath']
        outPath = files[file]['outPath']    
           
        with open(fullPath, 'rb') as f:
            byteData = f.read()

        mutableBytes = bytearray(byteData) 

        for enemy in enemiesByFile[fullPath]:           
            for attr, offset in enemy.attrOffsetDict.items():
                editBytes(mutableBytes, enemy, attr, offset)                                                   
                                               
        with open(outPath, 'wb') as f:
            f.write(mutableBytes)              


# TODO add code to handle editing byte data for float values
def editBytes(mutableBytes, enemy, attr, offset):
    enemyType = enemy.enemyType
                
    # Original slice of four bytes in data that we will edit
    fourBytesToEdit = mutableBytes[offset:(offset + 4)]                    

    # Convert those four bytes to an integer
    numFromBytes = int.from_bytes(fourBytesToEdit, byteorder='little', signed=True)                    

    newStatValue = round(numFromBytes * multipliersDict[enemyType][attr])
                            
    newStatValue = min(newStatValue, 2147483647)                 

    # new Stat value to 4 byte string
    bytesToInsert = newStatValue.to_bytes(4, byteorder='little', signed=True)                    

    # Insert new byte slice into mutable byte array
    mutableBytes[offset:(offset + 4)] = bytesToInsert


def debugEdits():
    with open("yaml files\\preStats-for-debugging.yaml", 'r') as file:
        preStatsData = yaml.load(file, Loader=yaml.FullLoader) 

    
    # iterate through all stats; use matching multiplier for assert statement
