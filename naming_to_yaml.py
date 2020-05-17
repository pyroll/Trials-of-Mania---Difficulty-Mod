import yaml

with open('yaml files\\preStats-for-debugging.yaml') as f:
    preNames = yaml.load(f, Loader=yaml.FullLoader)

# our dict for new yaml file
namesSeparated = {}

# # TODO fix entries like 'BIRD' using multiple enemies
# namesSeparated['ARMORNIGHT'] = []
# namesSeparated['ASSASSINBUG'] = []
# namesSeparated['ArchDemon'] = []
# namesSeparated['Altar'] = []
# namesSeparated['Arms'] = []
# namesSeparated['BARETTE'] = []
# namesSeparated['BASILISK'] = []
# namesSeparated['BATTOM'] = []
# namesSeparated['BEASTMASTER'] = []
# namesSeparated['BIRD'] = []
# namesSeparated['BLACKFANG'] = []
# namesSeparated['BLOODYWOLF'] = []
# namesSeparated['BOULDER'] = []
# namesSeparated['BOULDER'] = []

# for name in preNames:
#     if 'ARMORNIGHT' in name:        
#         namesSeparated['ARMORNIGHT'].append(name)
#     if 'ASSASSINBUG' in name:
#         namesSeparated['ASSASSINBUG'].append(name)
#     if 'Altar' in name:
#         namesSeparated['Altar'].append(name)
#     if 'ArchDemon' in name:
#         namesSeparated['ArchDemon'].append(name)
#     if name[:3] == 'Arm':
#         namesSeparated['Arms'].append(name)
#     if 'BARETTE' in name:
#         namesSeparated['BARETTE'].append(name)
#     if 'BASILISK' in name:
#         namesSeparated['BASILISK'].append(name)
#     if 'BATTOM' in name:
#         namesSeparated['BATTOM'].append(name)
#     if 'BEASTMASTER' in name:
#         namesSeparated['BEASTMASTER'].append(name)
#     if 'BIRD' in name:
#         namesSeparated['BIRD'].append(name)
#     if 'BLACKFANG' in name:
#         namesSeparated['BLACKFANG'].append(name)
#     if 'BLOODYWOLF' in name:
#         namesSeparated['BLOODYWOLF'].append(name)
#     if 'BOULDER' in name:
#         namesSeparated['BOULDER'].append(name)

# names that aren't grouped with anything
namesSeparated['Anise'] = []
namesSeparated['Anise Avatar'] = []
namesSeparated['AniseDragon']= []
namesSeparated['Beast Ruger']= []
namesSeparated['BeastKing']= []
namesSeparated['BlackKnight'] = []
namesSeparated['BlackRabi'] = []
namesSeparated['COCKABIRD_GROWTH_Lv65'] = []
namesSeparated['COCKATRICE'] = []
namesSeparated['Crystal'] = []
namesSeparated['DarkRich'] = []
namesSeparated['EAGLE'] = []
namesSeparated['Earl of evil eye'] = []
namesSeparated['Fallen saint'] = []
namesSeparated['HighWizard'] = []
namesSeparated['HugeDragon'] = []
namesSeparated['JewelryBeast'] = []
namesSeparated['KARL'] = []
namesSeparated['ManaStone Black'] = []
namesSeparated['ManaStone Earth'] = []
namesSeparated['ManaStone Fire'] = []
namesSeparated['ManaStone Water'] = []
namesSeparated['ManaStone Wind'] = []
namesSeparated['MiniBlackRabi'] = []
namesSeparated['Roki'] = []
namesSeparated['SHADOWZERO'] = []
namesSeparated['SpiralMoon_Gimmick01'] = []
namesSeparated['two'] = []

# TODO check 'CARMILL' in 'CARMILLA':
# 'Gigaburn_Gimmick' should be 3
# 'HellSouthernCross_Gimick' should be 2
# MachineGolem should be 2
# 'Man - eating death' should be 2
repeatedNames = ['ARMORNIGHT', 'ASSASSINBUG', 'Altar', 'ArchDemon', 'Arm',
                 'BARETTE', 'BASILISK', 'BATTOM', 'BEASTMASTER',
                 'BIRD', 'BLACKFANG', 'BLOODYWOLF', 'BOULDER',
                 'BOUNDWOLF', 'Ben', 'Bill', 'Bill and Ben',
                 'Body', 'Bruiser', 'CARMILLA', 'COCKATBIRD',
                 'CrimsonWizard', 'DARKBATTOM', 'DARKLORD',
                 'DARKPRIEST', 'DARTHMATANGO', 'DEATHMACHINE',
                 'DUCKGENERAL', 'DUCKSOLDIER', 'Dangard',
                 'Doran', 'ELEMENTSWORD', 'EVILSHERMAN', 'EVILSWORD',
                 'Eagle', 'Eye', 'FIREDRAKE', 'FROSTDRAGON', 'Feegu Mund',
                 'Flower', 'FullmetalHugger', 'GALBEE', 'GHOST', 'GHOUL',
                 'GIGACRAWLER', 'GOBLIN', 'GOBLINLORD', 'GOLDBARETTE', 'GOLDUNICO',
                 'GREATDAEMON', 'GREATDAEMON_SUMMON', 'GREATRABI', 'GRELL', 'GRELLMAGE', 'GREMLINS',
                 'GREMLINS_SUMMON', 'GUARDIAN',
                 'Genoa', 'Gigaburn_Gimmick', 'Gorva', 'GreadDeamon', 'Guilder Vine', 'HARPY',
                 'HIGHWIZARD', 'HandLB', 'HandRB', 'Head', 'HellSouthernCross_Gimick',
                 'Jewel Eater', 'KAISERMIMIC', 'KERBEROS', 'KINGRABI', 'KNIGHTBLADE', 'Karl',
                 'LADYBEE', 'LESSERDAEMON', 'LITTLEDEVIL', 'Land amber', 'Light Geizer',
                 'MACHINEGOLEM', 'MAGICIAN', 'MAIKONIDO', 'MALLBEAR', 'MAMAPOT', 'MEGACRAWLER',
                 'MachineGolem', 'Mispolm', 'NECROMANCER', 'NEEDLEBIRD', 'NIDORION', 'NINJA',
                 'NINJAMASTER', 'Neck', 'None', 'OGREBOX', 'PAKKUNDRAGON', 'PAKKUNOTAMA',
                 'PAKKUNTOKAGE', 'PAKKURIOTAMA', 'PAPAPOT', 'PETIDRAZOMBIE', 'PETITDRAGON', 
                 'PETITIAMATT', 'PETITPOSEIDON', 'POROBINHOOD', 'POROBINLEADER', 'PORON',
                 'POT', 'POWERBOULDER', 'QUEENBEE', 'RABI', 'RABIRION', 'RASTERBUG',
                 'RouletteDeath', 'SAHAGIN', 'SAHUAGIN', 'SEADRAGON', 'SEASERPENT',
                 'SEIREN', 'SHADOWZEROP1', 'SHADOWZEROP2', 'SHADOWZEROP3', 'SHADOWZEROP4',
                 'SHADOWZEROP5', 'SHADOWZEROP6', 'SHADOWZERO', 'SHAPE', 'SHAPESHIFTER',
                 'SHELLHUNTER', 'SILVERNIGHT', 'SILVERWOLF', 'SLIME', 'SLIMEPRINCE',
                 'SPECTRE', 'SUMMON_GHOST', 'SUMMON_GHOUL', 'SUMMON_GOLDBARETTE', 'SUMMON_GREATDAEMON',
                 'SUMMON_GREMLINS_Lv56', 'SUMMON_KERBEROS', 'SUMMON_LITTLEDEVIL',
                 'SUMMON_PAPAPOT', 'SUMMON_RABI', 'SUMMON_SAHUAGIN', 'SUMMON_ZOMBIE',
                 'SWORDMASTER', 'SWORDNIGHT', 'Sablehor', 'Shadow', 'ShadowDummy1',
                 'ShadowDummy2', 'ShadowDummy3', 'ShadowDummy4', 'ShadowDummy5',
                 'Tail', 'UNICORNHEAD', 'UNUSED', 'WEREWOLF', 'WIZARD', 'WOLFDEVIL',
                 'ZOMBIE', 'Zan Bie', 'Zhenker']

for name in repeatedNames:
    namesSeparated[name] = []

for name in preNames:
    for repName in repeatedNames:
        if repName in name:
            if repName == 'RABI' and 'RABIRION' in name:                
                continue
            if repName == 'ARMORNIGHT' and 'UNUSED' in name:
                continue
            if repName == 'Arm' and 'ArchDemon' in name:
                continue
            if repName == 'BARETTE' and ('GOLDBARETTE' in name or 'SUMMON_GOLDBARETTE' in name):
                continue
            if repName == 'BATTOM' and 'DARKBATTOM' in name:
                continue
            if repName == 'BIRD' and ('COCKABIRD' in name or 'COCKATBIRD' in name or 'NEEDLEBIRD' in name):
                continue
            if repName == 'BOULDER' and 'POWERBOULDER' in name:
                continue
            if repName == 'CARMILLA' and 'CARMILLAQUEEN' in name:
                continue
            if repName == 'COCKATBIRD' and 'COCKATBIRD_SUMMON' in name:
                continue
            if repName == 'GHOST' and 'SUMMON_GHOST' in name:
                continue
            if repName == 'GHOUL' and 'SUMMON_GHOUL' in name:
                continue
            if repName == 'GOBLIN' and ('GOBLINLORD' in name or 'UNUSED' in name):
                continue
            if repName == 'GOBLINLORD' and 'UNUSED' in name:
                continue
            if repName == 'GOLDBARETTE' and 'SUMMON' in name:
                continue
            if repName == 'GREATDAEMON' and 'SUMMON' in name:
                continue
            if repName == 'GRELL' and 'GRELLMAGE' in name:
                continue
            if repName == 'GREMLINS' and 'SUMMON' in name:
                continue
            if repName == 'HARPY' and 'UNUSED' in name:
                continue
            if repName == 'KERBEROS' and 'SUMMON' in name:
                continue
            if repName == 'LITTLEDEVIL' and 'SUMMON' in name:
                continue
            if repName == 'NINJA' and 'NINJAMASTER' in name:
                continue
            if repName == 'PAPAPOT' and 'SUMMON' in name:
                continue
            if repName == 'POT' and ('MAMAPOT' in name or 'PAPAPOT' in name or 'SUMMON' in name):
                continue
            if repName == 'RABI' and ('GREATRABI' in name or 'KINGRABI' in name or 'SUMMON' in name or 'UNUSED' in name):
                continue
            if repName == 'SAHUAGIN' and 'SUMMON' in name:
                continue
            if repName == 'SHAPE' and 'SHAPESHIFTER' in name:
                continue
            if repName == 'SLIME' and 'SLIMEPRINCE' in name:
                continue
            if repName == 'WIZARD' and 'HIGHWIZARD' in name:
                continue
            if repName == 'ZOMBIE' and ('PETIDRAZOMBIE' in name or 'SUMMON' in name):
                continue
            if repName == 'GALBEE' and 'UNUSED' in name:
                continue
            else:
                namesSeparated[repName].append(name)
            # break

# TODO access namesSeparated and remove keys that are actually
# separate enemies

with open('testing-names.yaml', 'w') as f:
    yaml.dump(namesSeparated, f)