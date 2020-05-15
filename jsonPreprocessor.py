import os
import yaml
from collections import defaultdict


def preprocessJson():
    rootdir = r'JSON Game Files\Trials of Mana\Content\Game00'

    # Walk through each directory in rootDirdict; get full path of file to use
    for root, dirs, files in os.walk(rootdir):
        for file in files:            
            
            # This will concatenate the 'head' and 'tail' to form the full file path
            fullPath = os.path.join(root, file)
            
            # Check paths and jsonDir keys to give a type_id to each file
            for k, v in jsonDir.items():                
                if fullPath == v + "\\" + file:
                    type_id = k
                # else:
                #     raise Exception('No matching file paths')
            
            if 'common' in type_id:
                type_id = 'common'
            elif 'boss_eb' in type_id or 'shin_eb' in type_id:
                type_id = 'parts'

            # Fix for common and boss using the same root path
            if type_id == 'boss' and 'EnemyStatus' in file:
                type_id = 'common'                         

            jsonToParserDict[file]["fullPath"] = fullPath
            jsonToParserDict[file]["type_id"] = type_id      


baseJson = r'JSON Game Files\Trials of Mana\Content\Game00'
jsonDir = {
            'common_BP': baseJson + r'\BP\Enemy\Zako\Data',
            'common': baseJson + r'\Data\Csv\CharaData',
            'boss': baseJson + r'\Data\Csv\CharaData',
            'boss_eb03_01': baseJson + r'\BP\Enemy\Boss\eb03_01\Data',
            'boss_eb05_01': baseJson + r'\BP\Enemy\Boss\eb05_01\Data',
            'boss_eb07_01': baseJson + r'\BP\Enemy\Boss\eb07_01\Data',
            'boss_eb18_01': baseJson + r'\BP\Enemy\Boss\eb18_01\Data',
            'boss_eb22_01': baseJson + r'\BP\Enemy\Boss\eb22_01\Data',
            'boss_eb23_01': baseJson + r'\BP\Enemy\Boss\eb23_01\Data',
            'boss_eb26_01': baseJson + r'\BP\Enemy\Boss\eb26_01\Data',
            'boss_eb27_01': baseJson + r'\BP\Enemy\Boss\eb27_01\Data',
            'shinju': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList',
            'shin_eb11': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb11_Parts',
            'shin_eb12': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb12_Parts',
            'shin_eb13': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb13_Parts',
            'shin_eb14': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb14_Parts',
            'shin_eb15': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb15_Parts',
            'shin_eb16': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb16_Parts',
            'shin_eb17': baseJson + r'\Data\Csv\CharaData\ShinjuStatusTableList\eb17_Parts',
            'parts': baseJson + r'\Data\Csv\CharaData\Parts',
            }

jsonToParserDict = defaultdict(dict)

preprocessJson()  

jsonToParserDict = dict(jsonToParserDict)

with open("yaml files\\json-for-parsing.yaml", 'w') as file:
    yaml.dump(jsonToParserDict, file)