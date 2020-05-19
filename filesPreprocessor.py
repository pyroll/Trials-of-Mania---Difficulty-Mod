import os
import yaml
from collections import defaultdict

# from ene_clas import currentVersionTitle


def preprocessFiles():
    rootdir = r'Game Files\Trials of Mana\Content\Game00'

    # Walk through each directory in rootDirdict; get full path of file to use
    for root, dirs, files in os.walk(rootdir):
        for file in files:            
            
            # This will concatenate the 'head' and 'tail' to form the full file path
            fullPath = os.path.join(root, file)

            outPath = fullPath.replace('Game Files', 'Custom_TofMania - 0.5.1_P')

            filesToEditDict[file]["fullPath"] = fullPath
            filesToEditDict[file]["outPath"] = outPath        


filesToEditDict = defaultdict(dict)

preprocessFiles()  

filesToEditDict = dict(filesToEditDict)

with open("yaml files\\files-to-edit.yaml", 'w') as file:
    yaml.dump(filesToEditDict, file)