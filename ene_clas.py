import os
import time
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
            self.attrOffsetDict[attr] = offset


def editHexAll(enemyType):

    # Start for file iterating
    # TODO way to prevent errors when rootdir of one enemyType contains the rootdir of a subsequent one
    rootdir = rootDirDict[enemyType]

    # Get full path of file to use
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # This will concatenate the 'head' and 'tail' to form the full file path
            fullPath = os.path.join(subdir, file)
            
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
    print("base of directories is: " + head)
    if not os.path.exists(head):        
        print("and so it is created")
        os.makedirs(head)
        
    for enemy_type in ['common', 'boss', 'parts']:
        for key, ene_dir in dirs[enemy_type].items():
            path = head + "\\" + ene_dir
            if not os.path.exists(path):
                os.makedirs(path)
    
    head = head + "\\" + dirs['shinju']['base']
    # remove 'base' key to remove from our for loop
    dirs['shinju'].pop('base')
    for key, val in dirs['shinju'].items():
        path = head + "\\" + val
        if not os.path.exists(path):
            os.makedirs(path)


with open("offsets-config.yaml", 'r') as file:
    loadedOffsets = yaml.load(file, Loader=yaml.FullLoader)

# List of all instance lists which will include common enemies, bosses, boss limbs, etc.
enemyCategories = {"common": [], 
                   "boss"  : [],
                   "shinju": [],
                   "parts" : []}

rootDirDict = {"common": r'Game Files\uexp files\Orig', 
               # TODO TESTING boss path so it doesn't cause errors with "shinju" and "parts"
               "boss"  : r'Game Files\Boss\Orig\uexp files\BossStatusTable.uexp',
               "shinju": r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList',
               "parts" : r'Game Files\Boss\Orig\uexp files\Parts'}

# paths we want the edited files to output to for UnrealPak.exe
finDirPath_BP = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\BP\\Enemy\\Zako\\Data\\'
finDirPath_Data = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\'
finDirPath_Boss = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\'
finDirPath_shinju = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\ShinjuStatusTableList\\'
finDirPath_parts = 'Custom_TofMania - 0.3.2_P\\Trials of Mana\\Content\\Game00\\Data\\Csv\\CharaData\\Parts\\'


#region Enemy Instance Creation Start

# ****** EnemyStatusSt01_2 - *****

st1_2Path = r'Game Files\uexp files\Orig\EnemyStatusSt01_2.uexp'

BOUNDWOLF_Lv6 = Enemy("common", st1_2Path, 1690)


# ****** EnemyStatusSt02 - Rabite Forest*****

st2Path = r'Game Files\uexp files\Orig\EnemyStatusSt02.uexp'

RABI_Lv1 = Enemy("common", st2Path, 1690)
MAIKONIDO_Lv1 = Enemy("common", st2Path, 3269)
BOUNDWOLF_Lv1 = Enemy("common", st2Path, 4848)
ASSASSINBUG_Lv1 = Enemy("common", st2Path, 6427)
RABI_Lv3 = Enemy("common", st2Path, 8006)
MAIKONIDO_Lv3 = Enemy("common", st2Path, 9585)
ASSASSINBUG_Lv3 = Enemy("common", st2Path, 11164)
RABI_Lv14 = Enemy("common", st2Path, 12743)
RABIRION_Lv15 = Enemy("common", st2Path, 14322)
MAIKONIDO_Lv14 = Enemy("common", st2Path, 15901)
ASSASSINBUG_Lv14 = Enemy("common", st2Path, 17480)
SUMMON_RABI_Lv15 = Enemy("common", st2Path, 19059)


# ****** EnemyStatusSt03 - *****

st3Path = r'Game Files\uexp files\Orig\EnemyStatusSt03.uexp'

RABI_Lv4 = Enemy("common", st3Path, 1690)
MAIKONIDO_Lv4 = Enemy("common", st3Path, 3269)
BATTOM_Lv4 = Enemy("common", st3Path, 4848)
GOBLIN_Lv4_AXE = Enemy("common", st3Path, 6427)
RABI_Lv5 = Enemy("common", st3Path, 8006)
MAIKONIDO_Lv5 = Enemy("common", st3Path, 9585)
BATTOM_Lv5 = Enemy("common", st3Path, 11164)
GOBLIN_Lv5_ARMOR = Enemy("common", st3Path, 12743)
ZOMBIE_Lv5 = Enemy("common", st3Path, 14322)


# ****** EnemyStatusSt09 - *****  *** This is where I started using a script for creating the instances

st9Path = r'Game Files\uexp files\Orig\EnemyStatusSt09.uexp'

RABI_Lv8 = Enemy("common", st9Path, 1690)
BATTOM_Lv8 = Enemy("common", st9Path, 3269)
GOBLIN_Lv8 = Enemy("common", st9Path, 4848)
ASSASSINBUG_Lv8 = Enemy("common", st9Path, 6427)
PORON_Lv8 = Enemy("common", st9Path, 8006)
ZOMBIE_Lv8 = Enemy("common", st9Path, 9585)
PORON_Lv8_DART = Enemy("common", st9Path, 11164)


# ****** EnemyStatusSt10 - *****

st10Path = r'Game Files\uexp files\Orig\EnemyStatusSt10.uexp'

RABI_LV8 = Enemy("common", st10Path, 1690)
GOBLIN_LV8 = Enemy("common", st10Path, 3269)


# ****** EnemyStatusSt12 - *****

st12Path = r'Game Files\uexp files\Orig\EnemyStatusSt12.uexp'

GOBLIN_LV10 = Enemy("common", st12Path, 1690)
GOBLINLORD_LV10 = Enemy("common", st12Path, 3269)
MALLBEAR_LV10 = Enemy("common", st12Path, 4848)
BATTOM_LV10 = Enemy("common", st12Path, 6427)
SLIME_LV10 = Enemy("common", st12Path, 8006)
MAIKONIDO_LV10 = Enemy("common", st12Path, 9585)


# ****** EnemyStatusSt13 - *****

st13Path = r'Game Files\uexp files\Orig\EnemyStatusSt13.uexp'

RABI_Lv1 = Enemy("common", st13Path, 1690)
MAIKONIDO_Lv1 = Enemy("common", st13Path, 3269)
MALLBEAR_LV11 = Enemy("common", st13Path, 4848)
UNUSED_RABI_LV11 = Enemy("common", st13Path, 6427)
BATTOM_LV11 = Enemy("common", st13Path, 8006)
UNUSED_GOBLINLORD_LV11 = Enemy("common", st13Path, 9585)
ASSASSINBUG_LV11 = Enemy("common", st13Path, 11164)
UNUSED_GALBEE_LV11 = Enemy("common", st13Path, 12743)
MALLBEAR_LV12 = Enemy("common", st13Path, 14322)
GOBLINLORD_LV12 = Enemy("common", st13Path, 15901)
GALBEE_LV12 = Enemy("common", st13Path, 17480)
BATTOM_LV12 = Enemy("common", st13Path, 19059)
MALLBEAR_LV13 = Enemy("common", st13Path, 20638)
BATTOM_LV13 = Enemy("common", st13Path, 22217)
GALBEE_LV13 = Enemy("common", st13Path, 23796)
RABI_Lv13 = Enemy("common", st13Path, 25375)
ASSASSINBUG_LV13 = Enemy("common", st13Path, 26954)
GOBLINLORD_LV13 = Enemy("common", st13Path, 28533)
MALLBEAR_LV40 = Enemy("common", st13Path, 30112)
GOBLINLORD_LV40 = Enemy("common", st13Path, 31691)


# ****** EnemyStatusSt15 - *****

st15Path = r'Game Files\uexp files\Orig\EnemyStatusSt15.uexp'

UNICORNHEAD_LV13_arm = Enemy("common", st15Path, 1690)
MAGICIAN_LV13 = Enemy("common", st15Path, 3269)
MACHINEGOLEM_LV13 = Enemy("common", st15Path, 4848)
UNICORNHEAD_LV15_arm = Enemy("common", st15Path, 6427)
MAGICIAN_LV16 = Enemy("common", st15Path, 8006)
MACHINEGOLEM_LV15_arm = Enemy("common", st15Path, 9585)


# ****** EnemyStatusSt18 - *****

st18Path = r'Game Files\uexp files\Orig\EnemyStatusSt18.uexp'

# Removed a period from "Lv.15" for ZOMBIE that came from the JSON file
ZOMBIE_Lv15 = Enemy("common", st18Path, 1690)
NEEDLEBIRD_Lv14 = Enemy("common", st18Path, 3269)
LITTLEDEVIL_Lv14 = Enemy("common", st18Path, 4848)
HARPY_Lv14 = Enemy("common", st18Path, 6427)
ARMORNIGHT_Lv14 = Enemy("common", st18Path, 8006)
ARMORNIGHT_Lv14_A = Enemy("common", st18Path, 9585)
NEEDLEBIRD_Lv15 = Enemy("common", st18Path, 11164)
LITTLEDEVIL_Lv15 = Enemy("common", st18Path, 12743)
HARPY_Lv15 = Enemy("common", st18Path, 14322)
ARMORNIGHT_Lv15_A = Enemy("common", st18Path, 15901)
ARMORNIGHT_Lv16_A = Enemy("common", st18Path, 17480)


# ****** EnemyStatusSt21 - *****

st21Path = r'Game Files\uexp files\Orig\EnemyStatusSt21.uexp'

ZOMBIE_Lv16 = Enemy("common", st21Path, 1690)
NEEDLEBIRD_Lv16 = Enemy("common", st21Path, 3269)
LITTLEDEVIL_Lv16 = Enemy("common", st21Path, 4848)
HARPY_Lv16 = Enemy("common", st21Path, 6427)
ARMORNIGHT_Lv16 = Enemy("common", st21Path, 8006)
ARMORNIGHT_Lv17_ARMOR = Enemy("common", st21Path, 9585)


# ****** EnemyStatusSt22 - *****

st22Path = r'Game Files\uexp files\Orig\EnemyStatusSt22.uexp'

NINJA_Lv1 = Enemy("common", st22Path, 1690)
LITTLEDEVIL_Lv18 = Enemy("common", st22Path, 3269)
ARMORNIGHT_Lv18 = Enemy("common", st22Path, 4848)
ARMORNIGHT_Lv19_ARMOR = Enemy("common", st22Path, 6427)
NINJA_Lv18 = Enemy("common", st22Path, 8006)
NINJA_Lv19_OMITARMOR = Enemy("common", st22Path, 9585)
EVILSWORD_Lv18 = Enemy("common", st22Path, 11164)


# ****** EnemyStatusSt23 - *****

st23Path = r'Game Files\uexp files\Orig\EnemyStatusSt23.uexp'

ZOMBIE_Lv21 = Enemy("common", st23Path, 1690)
GHOUL_Lv23 = Enemy("common", st23Path, 3269)
SLIME_Lv21 = Enemy("common", st23Path, 4848)
LITTLEDEVIL_Lv21 = Enemy("common", st23Path, 6427)
SPECTRE_Lv21 = Enemy("common", st23Path, 8006)
OGREBOX_Lv21 = Enemy("common", st23Path, 9585)
ZOMBIE_Lv21_N = Enemy("common", st23Path, 11164)
GHOUL_Lv23_N = Enemy("common", st23Path, 12743)
SLIME_Lv21_N = Enemy("common", st23Path, 14322)
LITTLEDEVIL_Lv21_N = Enemy("common", st23Path, 15901)
SPECTRE_Lv21_N = Enemy("common", st23Path, 17480)


# ****** EnemyStatusSt24 - *****

st24Path = r'Game Files\uexp files\Orig\EnemyStatusSt24.uexp'

RABIRION_LV23 = Enemy("common", st24Path, 1690)
DARKPRIEST_LV23 = Enemy("common", st24Path, 3269)
COCKATRICE_LV23 = Enemy("common", st24Path, 4848)
GOBLINLORD_LV23 = Enemy("common", st24Path, 6427)
GALBEE_LV23 = Enemy("common", st24Path, 8006)
MAIKONIDO_LV23 = Enemy("common", st24Path, 9585)
MALLBEAR_LV23 = Enemy("common", st24Path, 11164)
COCKATBIRD_LV23 = Enemy("common", st24Path, 12743)
SUMMON_RABI_LV23 = Enemy("common", st24Path, 14322)


# ****** EnemyStatusSt26 - *****

st26Path = r'Game Files\uexp files\Orig\EnemyStatusSt26.uexp'

BATTOM_Lv25 = Enemy("common", st26Path, 1690)
GOBLINLORD_Lv25 = Enemy("common", st26Path, 3269)
DARKPRIEST_Lv25 = Enemy("common", st26Path, 4848)
GRELL_Lv25 = Enemy("common", st26Path, 6427)
PAKKUNOTAMA_Lv25 = Enemy("common", st26Path, 8006)
PAKKUNTOKAGE_Lv25 = Enemy("common", st26Path, 9585)
POT_Lv25 = Enemy("common", st26Path, 11164)
MAMAPOT_Lv25 = Enemy("common", st26Path, 12743)
OGREBOX_Lv25 = Enemy("common", st26Path, 14322)


# ****** EnemyStatusSt28 - *****

st28Path = r'Game Files\uexp files\Orig\EnemyStatusSt28.uexp'

RABI_Lv1 = Enemy("common", st28Path, 1690)
SAHAGIN_Lv1 = Enemy("common", st28Path, 3269)
WIZARD_Lv25 = Enemy("common", st28Path, 4848)
SAHAGIN_Lv25 = Enemy("common", st28Path, 6427)
POT_Lv25 = Enemy("common", st28Path, 8006)
MAMAPOT_Lv25 = Enemy("common", st28Path, 9585)
PAKKUNTOKAGE_Lv26 = Enemy("common", st28Path, 11164)
SEASERPENT_Lv26 = Enemy("common", st28Path, 12743)
WIZARD_Lv26 = Enemy("common", st28Path, 14322)
SAHAGIN_Lv26 = Enemy("common", st28Path, 15901)


# ****** EnemyStatusSt31 - *****

st31Path = r'Game Files\uexp files\Orig\EnemyStatusSt31.uexp'

BARETTE_LV29 = Enemy("common", st31Path, 1690)
GOLDBARETTE_LV30 = Enemy("common", st31Path, 3269)
COCKATRICE_LV29 = Enemy("common", st31Path, 4848)
DARKPRIEST_LV29 = Enemy("common", st31Path, 6427)
DUCKSOLDIER_LV29 = Enemy("common", st31Path, 8006)
BIRD_LV29 = Enemy("common", st31Path, 9585)
DUCKSOLDIER_LV30_ARMOR = Enemy("common", st31Path, 11164)


# ****** EnemyStatusSt33 - *****

st33Path = r'Game Files\uexp files\Orig\EnemyStatusSt33.uexp'

FIREDRAKE_LV29 = Enemy("common", st33Path, 1690)
DUCKGENERAL_LV29 = Enemy("common", st33Path, 3269)
NINJAMASTER_LV29 = Enemy("common", st33Path, 4848)
SWORDMASTER_LV29 = Enemy("common", st33Path, 6427)
DARKPRIEST_LV29 = Enemy("common", st33Path, 8006)
FIREDRAKE_LV43 = Enemy("common", st33Path, 9585)
DUCKGENERAL_LV43 = Enemy("common", st33Path, 11164)
NINJAMASTER_LV43 = Enemy("common", st33Path, 12743)
SWORDMASTER_LV43 = Enemy("common", st33Path, 14322)
DARKPRIEST_LV43 = Enemy("common", st33Path, 15901)


# ****** EnemyStatusSt35 - *****

st35Path = r'Game Files\uexp files\Orig\EnemyStatusSt35.uexp'

RABI_Lv1 = Enemy("common", st35Path, 1690)
BOUNDWOLF_Lv1 = Enemy("common", st35Path, 3269)
BOUNDWOLF_Lv31 = Enemy("common", st35Path, 4848)
WEREWOLF_Lv32 = Enemy("common", st35Path, 6427)
DARKBATTOM_Lv31 = Enemy("common", st35Path, 8006)
BLACKFANG_Lv32_OMITARMOR = Enemy("common", st35Path, 9585)
SPECTRE_Lv31 = Enemy("common", st35Path, 11164)
BOUNDWOLF_Lv30 = Enemy("common", st35Path, 12743)
WEREWOLF_Lv30 = Enemy("common", st35Path, 14322)
DARKBATTOM_Lv30 = Enemy("common", st35Path, 15901)
BLACKFANG_Lv30_OMITARMOR = Enemy("common", st35Path, 17480)
SPECTRE_Lv30 = Enemy("common", st35Path, 19059)


# ****** EnemyStatusSt37 - *****

st37Path = r'Game Files\uexp files\Orig\EnemyStatusSt37.uexp'

DARTHMATANGO_LV32 = Enemy("common", st37Path, 1690)
POROBINHOOD_LV32 = Enemy("common", st37Path, 3269)
ASSASSINBUG_LV32 = Enemy("common", st37Path, 4848)
LADYBEE_LV32 = Enemy("common", st37Path, 6427)
MEGACRAWLER_LV32 = Enemy("common", st37Path, 8006)
DARTHMATANGO_LV33 = Enemy("common", st37Path, 9585)
POROBINHOOD_LV33 = Enemy("common", st37Path, 11164)
ASSASSINBUG_LV33 = Enemy("common", st37Path, 12743)
LADYBEE_LV33 = Enemy("common", st37Path, 14322)
MEGACRAWLER_LV33 = Enemy("common", st37Path, 15901)


# ****** EnemyStatusSt40 - *****

st40Path = r'Game Files\uexp files\Orig\EnemyStatusSt40.uexp'

ARMORNIGHT_LV34 = Enemy("common", st40Path, 1690)
HARPY_LV34 = Enemy("common", st40Path, 3269)
NEEDLEBIRD_LV34 = Enemy("common", st40Path, 4848)
LITTLEDEVIL_LV34 = Enemy("common", st40Path, 6427)


# ****** EnemyStatusSt41 - *****

st41Path = r'Game Files\uexp files\Orig\EnemyStatusSt41.uexp'

KINGRABI_LV35 = Enemy("common", st41Path, 1690)
RABI_LV35 = Enemy("common", st41Path, 3269)
RABIRION_LV35 = Enemy("common", st41Path, 4848)
MACHINEGOLEM_LV36 = Enemy("common", st41Path, 6427)
WIZARD_LV36 = Enemy("common", st41Path, 8006)
DARKPRIEST_LV36 = Enemy("common", st41Path, 9585)
NINJAMASTER_LV36 = Enemy("common", st41Path, 11164)
BLACKFANG_LV36 = Enemy("common", st41Path, 12743)
BOUNDWOLF_LV36 = Enemy("common", st41Path, 14322)
KINGRABI_LV36 = Enemy("common", st41Path, 15901)
RABI_LV36 = Enemy("common", st41Path, 17480)
RABIRION_LV36 = Enemy("common", st41Path, 19059)
SUMMON_RABI_LV36 = Enemy("common", st41Path, 20638)


# ****** EnemyStatusSt43 - *****

st43Path = r'Game Files\uexp files\Orig\EnemyStatusSt43.uexp'

UNICORNHEAD_Lv37 = Enemy("common", st43Path, 1690)
MAGICIAN_Lv37 = Enemy("common", st43Path, 3269)
WIZARD_Lv38 = Enemy("common", st43Path, 4848)
MACHINEGOLEM_Lv37 = Enemy("common", st43Path, 6427)
WIZARD_Lv39_OMITARMOR = Enemy("common", st43Path, 8006)
MACHINEGOLEM_Lv40 = Enemy("common", st43Path, 9585)


# ****** EnemyStatusSt44 - *****

st44Path = r'Game Files\uexp files\Orig\EnemyStatusSt44.uexp'

BOUNDWOLF_LV37 = Enemy("common", st44Path, 1690)
WEREWOLF_LV37 = Enemy("common", st44Path, 3269)
BLACKFANG_LV37 = Enemy("common", st44Path, 4848)
SILVERWOLF_LV37 = Enemy("common", st44Path, 6427)


# ****** EnemyStatusSt45 - *****

st45Path = r'Game Files\uexp files\Orig\EnemyStatusSt45.uexp'

NINJA_LV1 = Enemy("common", st45Path, 1690)
NINJA_LV37 = Enemy("common", st45Path, 3269)
NINJAMASTER_LV37 = Enemy("common", st45Path, 4848)
DARKPRIEST_LV37 = Enemy("common", st45Path, 6427)
LESSERDAEMON_LV37 = Enemy("common", st45Path, 8006)
NINJAMASTER_LV38 = Enemy("common", st45Path, 9585)


# ****** EnemyStatusSt47 - *****

st47Path = r'Game Files\uexp files\Orig\EnemyStatusSt47.uexp'

GIGACRAWLER_LV47 = Enemy("common", st47Path, 1690)
QUEENBEE_LV47 = Enemy("common", st47Path, 3269)
DARTHMATANGO_LV47 = Enemy("common", st47Path, 4848)
POROBINLEADER_LV47 = Enemy("common", st47Path, 6427)


# ****** EnemyStatusSt51 - *****

st51Path = r'Game Files\uexp files\Orig\EnemyStatusSt51.uexp'

BASILISK_LV53 = Enemy("common", st51Path, 1690)
PETITIAMATT_LV53 = Enemy("common", st51Path, 3269)
BOULDER_LV53 = Enemy("common", st51Path, 4848)
GUARDIAN_LV53 = Enemy("common", st51Path, 6427)
RASTERBUG_LV53 = Enemy("common", st51Path, 8006)
GREMLINS_LV53 = Enemy("common", st51Path, 9585)
LESSERDAEMON_LV53 = Enemy("common", st51Path, 11164)
KNIGHTBLADE_LV53 = Enemy("common", st51Path, 12743)
COCKATRICE_SUMMON_LV53 = Enemy("common", st51Path, 14322)
COCKATBIRD_SUMMON_LV53 = Enemy("common", st51Path, 15901)
BASILISK_LV54 = Enemy("common", st51Path, 17480)
PETITIAMATT_LV54 = Enemy("common", st51Path, 19059)
BOULDER_LV54 = Enemy("common", st51Path, 20638)
GUARDIAN_LV54 = Enemy("common", st51Path, 22217)
RASTERBUG_LV54 = Enemy("common", st51Path, 23796)
GREMLINS_LV54 = Enemy("common", st51Path, 25375)
LESSERDAEMON_LV54 = Enemy("common", st51Path, 26954)
KNIGHTBLADE_LV54 = Enemy("common", st51Path, 28533)
COCKATRICE_SUMMON_LV54 = Enemy("common", st51Path, 30112)
COCKATBIRD_SUMMON_LV54 = Enemy("common", st51Path, 31691)
GUARDIAN_LONG_LV53 = Enemy("common", st51Path, 33270)
GREMLINS_LONG_LV53 = Enemy("common", st51Path, 34849)
KNIGHTBLADE_LONG_LV53 = Enemy("common", st51Path, 36428)
LESSERDAEMON_LONG_LV53 = Enemy("common", st51Path, 38007)
RASTERBUG_LONG_LV53 = Enemy("common", st51Path, 39586)
GUARDIAN_LONG_LV54 = Enemy("common", st51Path, 41165)
GREMLINS_LONG_LV54 = Enemy("common", st51Path, 42744)
KNIGHTBLADE_LONG_LV54 = Enemy("common", st51Path, 44323)
LESSERDAEMON_LONG_LV54 = Enemy("common", st51Path, 45902)
RASTERBUG_LONG_LV54 = Enemy("common", st51Path, 47481)
PETITIAMATT_ARMOR_LV54 = Enemy("common", st51Path, 49060)
LESSERDAEMON_ARMOR_LV54 = Enemy("common", st51Path, 50639)
LESSERDAEMON_ARMOR_LONG_LV54 = Enemy("common", st51Path, 52218)


# ****** EnemyStatusSt52 - *****

st52Path = r'Game Files\uexp files\Orig\EnemyStatusSt52.uexp'

HIGHWIZARD_Lv55 = Enemy("common", st52Path, 1690)
DEATHMACHINE_Lv55 = Enemy("common", st52Path, 3269)
DARKLORD_Lv55 = Enemy("common", st52Path, 4848)
PAPAPOT_Lv55 = Enemy("common", st52Path, 6427)
PETITDRAGON_Lv55 = Enemy("common", st52Path, 8006)
FROSTDRAGON_Lv55 = Enemy("common", st52Path, 9585)
PETITIAMATT_Lv55 = Enemy("common", st52Path, 11164)
POWERBOULDER_Lv55 = Enemy("common", st52Path, 12743)
HIGHWIZARD_Lv56 = Enemy("common", st52Path, 14322)
DEATHMACHINE_Lv56 = Enemy("common", st52Path, 15901)
DARKLORD_Lv56 = Enemy("common", st52Path, 17480)
PAPAPOT_Lv56 = Enemy("common", st52Path, 19059)
HIGHWIZARD_Lv58 = Enemy("common", st52Path, 20638)
DEATHMACHINE_Lv58 = Enemy("common", st52Path, 22217)
PETITDRAGON_Lv58 = Enemy("common", st52Path, 23796)
FROSTDRAGON_Lv58 = Enemy("common", st52Path, 25375)
PETITIAMATT_Lv58 = Enemy("common", st52Path, 26954)
PETIDRAZOMBIE_Lv58 = Enemy("common", st52Path, 28533)
POWERBOULDER_Lv58 = Enemy("common", st52Path, 30112)
GREATDAEMON_Lv58 = Enemy("common", st52Path, 31691)
KAISERMIMIC_Lv58 = Enemy("common", st52Path, 33270)
HIGHWIZARD_Lv59 = Enemy("common", st52Path, 34849)
DEATHMACHINE_Lv59 = Enemy("common", st52Path, 36428)
PETITDRAGON_Lv59 = Enemy("common", st52Path, 38007)
FROSTDRAGON_Lv59 = Enemy("common", st52Path, 39586)
PETITIAMATT_Lv59 = Enemy("common", st52Path, 41165)
GREATDAEMON_Lv59 = Enemy("common", st52Path, 42744)
HIGHWIZARD_Lv60 = Enemy("common", st52Path, 44323)
DEATHMACHINE_Lv60 = Enemy("common", st52Path, 45902)
DARKLORD_Lv60 = Enemy("common", st52Path, 47481)
PAPAPOT_Lv60 = Enemy("common", st52Path, 49060)
PETITDRAGON_Lv60 = Enemy("common", st52Path, 50639)
FROSTDRAGON_Lv60 = Enemy("common", st52Path, 52218)
PETITIAMATT_Lv60 = Enemy("common", st52Path, 53797)
PETIDRAZOMBIE_Lv60 = Enemy("common", st52Path, 55376)
POWERBOULDER_Lv60 = Enemy("common", st52Path, 56955)
GREATDAEMON_Lv60 = Enemy("common", st52Path, 58534)
PETIDRAZOMBIE_Lv61 = Enemy("common", st52Path, 60113)
GREATDAEMON_Lv61 = Enemy("common", st52Path, 61692)
PETIDRAZOMBIE_ARMOR_Lv61 = Enemy("common", st52Path, 63271)
GREATDAEMON_ARMOR_Lv61 = Enemy("common", st52Path, 64850)


# ****** EnemyStatusSt53 - *****

st53Path = r'Game Files\uexp files\Orig\EnemyStatusSt53.uexp'

GREATRABI_Lv53 = Enemy("common", st53Path, 1690)
RASTERBUG_Lv53 = Enemy("common", st53Path, 3269)
UNICORNHEAD_Lv53 = Enemy("common", st53Path, 4848)
MAGICIAN_Lv53 = Enemy("common", st53Path, 6427)
GUARDIAN_Lv53 = Enemy("common", st53Path, 8006)
ARMORNIGHT_Lv53 = Enemy("common", st53Path, 9585)
NINJA_Lv53 = Enemy("common", st53Path, 11164)
EVILSWORD_Lv53 = Enemy("common", st53Path, 12743)
EVILSHERMAN_Lv53 = Enemy("common", st53Path, 14322)
PAPAPOT_Lv53 = Enemy("common", st53Path, 15901)
WOLFDEVIL_Lv53 = Enemy("common", st53Path, 17480)
BOULDER_Lv53 = Enemy("common", st53Path, 19059)
LESSERDAEMON_Lv53 = Enemy("common", st53Path, 20638)
GREATDAEMON_SUMMON_Lv53 = Enemy("common", st53Path, 22217)
LITTLEDEVIL_SUMMON_Lv53 = Enemy("common", st53Path, 23796)
GREMLINS_SUMMON_Lv53 = Enemy("common", st53Path, 25375)


# ****** EnemyStatusSt54 - *****

st54Path = r'Game Files\uexp files\Orig\EnemyStatusSt54.uexp'

DEATHMACHINE_LV56 = Enemy("common", st54Path, 1690)
ELEMENTSWORD_LV56 = Enemy("common", st54Path, 3269)
DARKPRIEST_LV56 = Enemy("common", st54Path, 4848)
GHOST_LV56 = Enemy("common", st54Path, 6427)
NECROMANCER_LV56 = Enemy("common", st54Path, 8006)
PETIDRAZOMBIE_LV56 = Enemy("common", st54Path, 9585)
CARMILLAQUEEN_Lv56 = Enemy("common", st54Path, 11164)
POWERBOULDER_Lv56 = Enemy("common", st54Path, 12743)
GREATDAEMON_Lv56 = Enemy("common", st54Path, 14322)
DEATHMACHINE_LV58 = Enemy("common", st54Path, 15901)
ELEMENTSWORD_LV58 = Enemy("common", st54Path, 17480)
NECROMANCER_LV58 = Enemy("common", st54Path, 19059)
PETIDRAZOMBIE_LV58 = Enemy("common", st54Path, 20638)
CARMILLAQUEEN_Lv58_OMITARMOR = Enemy("common", st54Path, 22217)
POWERBOULDER_Lv58 = Enemy("common", st54Path, 23796)
GREATDAEMON_Lv58_ARMOR = Enemy("common", st54Path, 25375)
UNICORNHEAD_LV56 = Enemy("common", st54Path, 26954)
BOUNDWOLF_LV56 = Enemy("common", st54Path, 28533)
ZOMBIE_LV56 = Enemy("common", st54Path, 30112)
GHOUL_LV57 = Enemy("common", st54Path, 31691)
SPECTRE_LV56 = Enemy("common", st54Path, 33270)
GHOST_LV58 = Enemy("common", st54Path, 34849)
ASSASSINBUG_LV56 = Enemy("common", st54Path, 36428)
POROBINHOOD_LV56 = Enemy("common", st54Path, 38007)
LADYBEE_LV56 = Enemy("common", st54Path, 39586)
MEGACRAWLER_LV56 = Enemy("common", st54Path, 41165)
LITTLEDEVIL_LV56 = Enemy("common", st54Path, 42744)
ARMORNIGHT_LV56 = Enemy("common", st54Path, 44323)
NINJA_LV56 = Enemy("common", st54Path, 45902)
EVILSWORD_LV56 = Enemy("common", st54Path, 47481)
SILVERWOLF_LV56 = Enemy("common", st54Path, 49060)
BLOODYWOLF_LV57 = Enemy("common", st54Path, 50639)
CARMILLA_LV56 = Enemy("common", st54Path, 52218)
BATTOM_LV56 = Enemy("common", st54Path, 53797)
GOBLINLORD_LV56 = Enemy("common", st54Path, 55376)
GRELL_LV56 = Enemy("common", st54Path, 56955)
KAISERMIMIC_Lv58 = Enemy("common", st54Path, 58534)
SUMMON_ZOMBIE_LV56 = Enemy("common", st54Path, 60113)
SUMMON_GHOUL_LV56 = Enemy("common", st54Path, 61692)
SUMMON_GHOST_LV56 = Enemy("common", st54Path, 63271)
SUMMON_ZOMBIE_LV58 = Enemy("common", st54Path, 64850)
SUMMON_GHOUL_LV58 = Enemy("common", st54Path, 66429)
SUMMON_GHOST_LV58 = Enemy("common", st54Path, 68008)


# ****** EnemyStatusSt55 - *****

st55Path = r'Game Files\uexp files\Orig\EnemyStatusSt55.uexp'

KERBEROS_Lv53 = Enemy("common", st55Path, 1690)
GREMLINS_Lv53 = Enemy("common", st55Path, 3269)
KNIGHTBLADE_Lv53 = Enemy("common", st55Path, 4848)
GHOST_Lv53 = Enemy("common", st55Path, 6427)
WOLFDEVIL_Lv53 = Enemy("common", st55Path, 8006)
PETITIAMATT_Lv53 = Enemy("common", st55Path, 9585)
BOULDER_Lv53 = Enemy("common", st55Path, 11164)
LESSERDAEMON_Lv53 = Enemy("common", st55Path, 12743)
KNIGHTBLADE_Lv55_OMITARMOR = Enemy("common", st55Path, 14322)
LESSERDAEMON_Lv55_ARMOR = Enemy("common", st55Path, 15901)


# ****** EnemyStatusSt56 - *****

st56Path = r'Game Files\uexp files\Orig\EnemyStatusSt56.uexp'

GOLDUNICO_Lv56 = Enemy("common", st56Path, 1690)
HIGHWIZARD_Lv56 = Enemy("common", st56Path, 3269)
DARKLORD_Lv56 = Enemy("common", st56Path, 4848)
ELEMENTSWORD_Lv56 = Enemy("common", st56Path, 6427)
EVILSHERMAN_Lv56 = Enemy("common", st56Path, 8006)
CARMILLAQUEEN_Lv56 = Enemy("common", st56Path, 9585)
POWERBOULDER_Lv56 = Enemy("common", st56Path, 11164)
GREATDAEMON_Lv56 = Enemy("common", st56Path, 12743)
KAISERMIMIC_Lv58 = Enemy("common", st56Path, 14322)
GOLDUNICO_Lv58_ARMOR = Enemy("common", st56Path, 15901)
DARKLORD_Lv58_ARMOR = Enemy("common", st56Path, 17480)
CARMILLAQUEEN_Lv58_OMITARMOR = Enemy("common", st56Path, 19059)
GREATDAEMON_Lv58_ARMOR = Enemy("common", st56Path, 20638)
SUMMON_LITTLEDEVIL_Lv56 = Enemy("common", st56Path, 22217)
SUMMON_GREMLINS_Lv56 = Enemy("common", st56Path, 23796)
SUMMON_GREATDAEMON_Lv56 = Enemy("common", st56Path, 25375)


# ****** EnemyStatusSt57 - *****

st57Path = r'Game Files\uexp files\Orig\EnemyStatusSt57.uexp'

SHAPESHIFTER_LV62 = Enemy("common", st57Path, 1690)
SHADOWZERO_LV63 = Enemy("common", st57Path, 3269)
SHAPESHIFTER_LV61 = Enemy("common", st57Path, 4848)


# ****** EnemyStatusSt67 - *****

st67Path = r'Game Files\uexp files\Orig\EnemyStatusSt67.uexp'

KERBEROS_Lv64 = Enemy("common", st67Path, 1690)
HIGHWIZARD_Lv64 = Enemy("common", st67Path, 3269)
DEATHMACHINE_Lv64 = Enemy("common", st67Path, 4848)
DARKLORD_Lv64 = Enemy("common", st67Path, 6427)
PETITIAMATT_Lv64 = Enemy("common", st67Path, 8006)
GREATDAEMON_Lv64 = Enemy("common", st67Path, 9585)


# ****** EnemyStatusSt67_A - *****

st67_APath = r'Game Files\uexp files\Orig\EnemyStatusSt67_A.uexp'

RASTERBUG_Lv64 = Enemy("common", st67_APath, 1690)
SLIMEPRINCE_Lv64 = Enemy("common", st67_APath, 3269)
NIDORION_Lv64 = Enemy("common", st67_APath, 4848)
QUEENBEE_Lv64 = Enemy("common", st67_APath, 6427)
BASILISK_Lv64 = Enemy("common", st67_APath, 8006)
GIGACRAWLER_Lv64 = Enemy("common", st67_APath, 9585)
COCKATRICE_SUMMON_Lv64 = Enemy("common", st67_APath, 11164)
COCKATBIRD_SUMMON_Lv64 = Enemy("common", st67_APath, 12743)


# ****** EnemyStatusSt67_B - *****

st67_BPath = r'Game Files\uexp files\Orig\EnemyStatusSt67_B.uexp'

WIZARD_Lv64 = Enemy("common", st67_BPath, 1690)
HIGHWIZARD_Lv64 = Enemy("common", st67_BPath, 3269)
SWORDNIGHT_Lv64 = Enemy("common", st67_BPath, 4848)
DARKLORD_Lv64 = Enemy("common", st67_BPath, 6427)
NINJAMASTER_Lv64 = Enemy("common", st67_BPath, 8006)
KNIGHTBLADE_Lv64 = Enemy("common", st67_BPath, 9585)
PETITDRAGON_Lv64 = Enemy("common", st67_BPath, 11164)
FROSTDRAGON_Lv64 = Enemy("common", st67_BPath, 12743)
PETITIAMATT_Lv64 = Enemy("common", st67_BPath, 14322)
PETIDRAZOMBIE_Lv64 = Enemy("common", st67_BPath, 15901)
KAISERMIMIC_Lv64 = Enemy("common", st67_BPath, 17480)


# ****** EnemyStatusSt67_C - *****

st67_CPath = r'Game Files\uexp files\Orig\EnemyStatusSt67_C.uexp'

COCKATRICE_Lv65 = Enemy("common", st67_CPath, 1690)
COCKABIRD_GROWTH_Lv65 = Enemy("common", st67_CPath, 3269)
GREMLINS_Lv65 = Enemy("common", st67_CPath, 4848)
NINJA_Lv65 = Enemy("common", st67_CPath, 6427)
NINJAMASTER_Lv65 = Enemy("common", st67_CPath, 8006)
KNIGHTBLADE_Lv65 = Enemy("common", st67_CPath, 9585)
EVILSHERMAN_Lv65 = Enemy("common", st67_CPath, 11164)
DUCKGENERAL_Lv65 = Enemy("common", st67_CPath, 12743)
GOLDBARETTE_Lv65 = Enemy("common", st67_CPath, 14322)
SHAPESHIFTER_Lv65 = Enemy("common", st67_CPath, 15901)
LITTLEDEVIL_SUMMON_Lv65 = Enemy("common", st67_CPath, 17480)
GREMLINS_SUMMON_Lv65 = Enemy("common", st67_CPath, 19059)
GREATDAEMON_SUMMON_Lv65 = Enemy("common", st67_CPath, 20638)


# ****** EnemyStatusSt67_E - *****

st67_EPath = r'Game Files\uexp files\Orig\EnemyStatusSt67_E.uexp'

ZOMBIE_Lv67 = Enemy("common", st67_EPath, 1690)
GHOUL_Lv67 = Enemy("common", st67_EPath, 3269)
SLIMEPRINCE_Lv67 = Enemy("common", st67_EPath, 4848)
GHOST_Lv67 = Enemy("common", st67_EPath, 6427)
NECROMANCER_Lv67 = Enemy("common", st67_EPath, 8006)
GRELLMAGE_Lv67 = Enemy("common", st67_EPath, 9585)
PAKKURIOTAMA_Lv67 = Enemy("common", st67_EPath, 11164)
PAKKUNDRAGON_Lv67 = Enemy("common", st67_EPath, 12743)
PETIDRAZOMBIE_Lv67 = Enemy("common", st67_EPath, 14322)
POWERBOULDER_Lv67 = Enemy("common", st67_EPath, 15901)
KAISERMIMIC_Lv67 = Enemy("common", st67_EPath, 17480)
ZOMBIE_Summon = Enemy("common", st67_EPath, 19059)
GHOUL_Summon = Enemy("common", st67_EPath, 20638)
GHOST_Summon = Enemy("common", st67_EPath, 22217)


# ****** EnemyStatusSt67_G - *****

st67_GPath = r'Game Files\uexp files\Orig\EnemyStatusSt67_G.uexp'

UNICORNHEAD_lv69 = Enemy("common", st67_GPath, 1690)
GOLDUNICO_lv69 = Enemy("common", st67_GPath, 3269)
HIGHWIZARD_lv69 = Enemy("common", st67_GPath, 4848)
GUARDIAN_lv69 = Enemy("common", st67_GPath, 6427)
DEATHMACHINE_lv69 = Enemy("common", st67_GPath, 8006)
PAPAPOT_lv69 = Enemy("common", st67_GPath, 9585)
SUMMON_SAHUAGIN_lv69 = Enemy("common", st67_GPath, 11164)
PETITPOSEIDON_lv69 = Enemy("common", st67_GPath, 12743)
SEADRAGON_lv69 = Enemy("common", st67_GPath, 14322)
FROSTDRAGON_LV69 = Enemy("common", st67_GPath, 15901)
SHADOWZERO_LV69 = Enemy("common", st67_GPath, 17480)
KAISERMIMIC = Enemy("common", st67_GPath, 19059)


# ****** EnemyStatusSt67_H - *****

st67_HPath = r'Game Files\uexp files\Orig\EnemyStatusSt67_H.uexp'

DARKBATTOM_lv69 = Enemy("common", st67_HPath, 1690)
BIRD_lv69 = Enemy("common", st67_HPath, 3269)
GREMLINS_lv69 = Enemy("common", st67_HPath, 4848)
SEIREN_lv69 = Enemy("common", st67_HPath, 6427)
ELEMENTSWORD_lv69 = Enemy("common", st67_HPath, 8006)
GIGACRAWLER_lv69 = Enemy("common", st67_HPath, 9585)
CARMILLAQUEEN_lv69 = Enemy("common", st67_HPath, 11164)
POWERBOULDER_lv69 = Enemy("common", st67_HPath, 12743)
LESSERDAEMON_lv69 = Enemy("common", st67_HPath, 14322)
GREATDAEMON_lv69 = Enemy("common", st67_HPath, 15901)
RABI_lv69 = Enemy("common", st67_HPath, 17480)
RABIRION_lv69 = Enemy("common", st67_HPath, 19059)
KINGRABI_lv69 = Enemy("common", st67_HPath, 20638)
GREATRABI_lv69 = Enemy("common", st67_HPath, 22217)
KAISERMIMIC_lv69 = Enemy("common", st67_HPath, 23796)
RABI_Summon = Enemy("common", st67_HPath, 25375)


# ****** EnemyStatusSt67_I - *****

st67_IPath = r'Game Files\uexp files\Orig\EnemyStatusSt67_I.uexp'

BEASTMASTER_lv71 = Enemy("common", st67_IPath, 1690)
KERBEROS_lv71 = Enemy("common", st67_IPath, 3269)
POROBINLEADER_lv71 = Enemy("common", st67_IPath, 4848)
FIREDRAKE_lv71 = Enemy("common", st67_IPath, 6427)
WEREWOLF_lv71 = Enemy("common", st67_IPath, 8006)
BLACKFANG_lv71 = Enemy("common", st67_IPath, 9585)
SILVERWOLF_lv71 = Enemy("common", st67_IPath, 11164)
BLOODYWOLF_lv71 = Enemy("common", st67_IPath, 12743)
WOLFDEVIL_lv71 = Enemy("common", st67_IPath, 14322)
GOLDBARETTE_Summon = Enemy("common", st67_IPath, 15901)
KERBEROS_Summon = Enemy("common", st67_IPath, 17480)


# ****** EnemyStatusStcustom - *****

stcustomPath = r'Game Files\uexp files\Orig\EnemyCustomStatusTable.uexp'

RABI_Lv1 = Enemy("common", stcustomPath, 1690)
RABI = Enemy("common", stcustomPath, 3269)
RABI = Enemy("common", stcustomPath, 4848)
RABI = Enemy("common", stcustomPath, 6427)
RABI_Lv3 = Enemy("common", stcustomPath, 9585)
RABI = Enemy("common", stcustomPath, 11164)
RABI = Enemy("common", stcustomPath, 12743)
RABI = Enemy("common", stcustomPath, 14322)
RABI = Enemy("common", stcustomPath, 15901)
RABI = Enemy("common", stcustomPath, 17480)
RABI = Enemy("common", stcustomPath, 19059)
RABI = Enemy("common", stcustomPath, 20638)
RABIRION = Enemy("common", stcustomPath, 22217)
RABIRION = Enemy("common", stcustomPath, 23796)
RABIRION = Enemy("common", stcustomPath, 25375)
KINGRABI = Enemy("common", stcustomPath, 26954)
GREATRABI = Enemy("common", stcustomPath, 28533)
MAIKONIDO = Enemy("common", stcustomPath, 30112)
MAIKONIDO = Enemy("common", stcustomPath, 31691)
MAIKONIDO = Enemy("common", stcustomPath, 33270)
MAIKONIDO = Enemy("common", stcustomPath, 34849)
MAIKONIDO = Enemy("common", stcustomPath, 36428)
MAIKONIDO = Enemy("common", stcustomPath, 38007)
MAIKONIDO = Enemy("common", stcustomPath, 39586)
DARTHMATANGO = Enemy("common", stcustomPath, 41165)
DARTHMATANGO = Enemy("common", stcustomPath, 53797)
BATTOM = Enemy("common", stcustomPath, 55376)
BATTOM = Enemy("common", stcustomPath, 56955)
BATTOM = Enemy("common", stcustomPath, 58534)
BATTOM = Enemy("common", stcustomPath, 60113)
BATTOM = Enemy("common", stcustomPath, 61692)
BATTOM = Enemy("common", stcustomPath, 63271)
BATTOM = Enemy("common", stcustomPath, 64850)
DARKBATTOM = Enemy("common", stcustomPath, 66429)
DARKBATTOM = Enemy("common", stcustomPath, 68008)
GOBLIN = Enemy("common", stcustomPath, 69587)
GOBLIN = Enemy("common", stcustomPath, 71166)
GOBLIN = Enemy("common", stcustomPath, 72745)
GOBLIN = Enemy("common", stcustomPath, 74324)
GOBLIN = Enemy("common", stcustomPath, 75903)
GOBLINLORD = Enemy("common", stcustomPath, 77482)
GOBLINLORD = Enemy("common", stcustomPath, 79061)
GOBLINLORD = Enemy("common", stcustomPath, 80640)
GOBLINLORD = Enemy("common", stcustomPath, 82219)
GOBLINLORD = Enemy("common", stcustomPath, 83798)
GOBLINLORD = Enemy("common", stcustomPath, 85377)
BEASTMASTER = Enemy("common", stcustomPath, 98009)
BEASTMASTER = Enemy("common", stcustomPath, 99588)
BOUNDWOLF = Enemy("common", stcustomPath, 101167)
BOUNDWOLF = Enemy("common", stcustomPath, 102746)
BOUNDWOLF = Enemy("common", stcustomPath, 104325)
BOUNDWOLF = Enemy("common", stcustomPath, 105904)
BOUNDWOLF = Enemy("common", stcustomPath, 107483)
BOUNDWOLF = Enemy("common", stcustomPath, 109062)
BOUNDWOLF = Enemy("common", stcustomPath, 110641)
KERBEROS = Enemy("common", stcustomPath, 123273)
KERBEROS = Enemy("common", stcustomPath, 124852)
ASSASSINBUG_Lv3 = Enemy("common", stcustomPath, 126431)
ASSASSINBUG = Enemy("common", stcustomPath, 128010)
ASSASSINBUG = Enemy("common", stcustomPath, 129589)
ASSASSINBUG = Enemy("common", stcustomPath, 131168)
ASSASSINBUG = Enemy("common", stcustomPath, 132747)
ASSASSINBUG = Enemy("common", stcustomPath, 134326)
RASTERBUG = Enemy("common", stcustomPath, 135905)
RASTERBUG = Enemy("common", stcustomPath, 137484)
PORON = Enemy("common", stcustomPath, 139063)
POROBINHOOD = Enemy("common", stcustomPath, 140642)
POROBINHOOD = Enemy("common", stcustomPath, 142221)
POROBINLEADER = Enemy("common", stcustomPath, 154853)
POROBINLEADER = Enemy("common", stcustomPath, 156432)
ZOMBIE = Enemy("common", stcustomPath, 159590)
ZOMBIE = Enemy("common", stcustomPath, 161169)
ZOMBIE = Enemy("common", stcustomPath, 162748)
ZOMBIE = Enemy("common", stcustomPath, 164327)
ZOMBIE = Enemy("common", stcustomPath, 165906)
ZOMBIE = Enemy("common", stcustomPath, 167485)
GHOUL = Enemy("common", stcustomPath, 169064)
GHOUL = Enemy("common", stcustomPath, 181696)
GHOUL = Enemy("common", stcustomPath, 183275)
SLIME = Enemy("common", stcustomPath, 184854)
SLIME = Enemy("common", stcustomPath, 186433)
SLIMEPRINCE = Enemy("common", stcustomPath, 199065)
MALLBEAR = Enemy("common", stcustomPath, 200644)
MALLBEAR = Enemy("common", stcustomPath, 202223)
MALLBEAR = Enemy("common", stcustomPath, 203802)
MALLBEAR = Enemy("common", stcustomPath, 205381)
NIDORION = Enemy("common", stcustomPath, 218013)
GALBEE = Enemy("common", stcustomPath, 219592)
GALBEE = Enemy("common", stcustomPath, 221171)
LADYBEE = Enemy("common", stcustomPath, 222750)
LADYBEE = Enemy("common", stcustomPath, 224329)
QUEENBEE = Enemy("common", stcustomPath, 236961)
UNICORNHEAD = Enemy("common", stcustomPath, 238540)
UNICORNHEAD = Enemy("common", stcustomPath, 240119)
UNICORNHEAD = Enemy("common", stcustomPath, 243277)
UNICORNHEAD = Enemy("common", stcustomPath, 244856)
GOLDUNICO = Enemy("common", stcustomPath, 246435)
GOLDUNICO = Enemy("common", stcustomPath, 248014)
MAGICIAN = Enemy("common", stcustomPath, 249593)
MAGICIAN = Enemy("common", stcustomPath, 251172)
WIZARD = Enemy("common", stcustomPath, 254330)
WIZARD = Enemy("common", stcustomPath, 255909)
WIZARD = Enemy("common", stcustomPath, 257488)
WIZARD = Enemy("common", stcustomPath, 259067)
HIGHWIZARD = Enemy("common", stcustomPath, 260646)
HIGHWIZARD = Enemy("common", stcustomPath, 262225)
HIGHWIZARD = Enemy("common", stcustomPath, 263804)
MACHINEGOLEM = Enemy("common", stcustomPath, 265383)
MACHINEGOLEM = Enemy("common", stcustomPath, 266962)
MACHINEGOLEM = Enemy("common", stcustomPath, 268541)
GUARDIAN = Enemy("common", stcustomPath, 270120)
GUARDIAN = Enemy("common", stcustomPath, 271699)
DEATHMACHINE = Enemy("common", stcustomPath, 273278)
DEATHMACHINE = Enemy("common", stcustomPath, 274857)
COCKATRICE = Enemy("common", stcustomPath, 276436)
COCKATRICE = Enemy("common", stcustomPath, 278015)
COCKATRICE = Enemy("common", stcustomPath, 290647)
COCKATRICE = Enemy("common", stcustomPath, 292226)
NEEDLEBIRD = Enemy("common", stcustomPath, 293805)
NEEDLEBIRD = Enemy("common", stcustomPath, 295384)
NEEDLEBIRD = Enemy("common", stcustomPath, 296963)
BIRD = Enemy("common", stcustomPath, 309595)
BIRD = Enemy("common", stcustomPath, 311174)
BIRD = Enemy("common", stcustomPath, 323806)
BIRD = Enemy("common", stcustomPath, 325385)
LITTLEDEVIL = Enemy("common", stcustomPath, 326964)
LITTLEDEVIL = Enemy("common", stcustomPath, 328543)
LITTLEDEVIL = Enemy("common", stcustomPath, 330122)
LITTLEDEVIL = Enemy("common", stcustomPath, 331701)
LITTLEDEVIL = Enemy("common", stcustomPath, 333280)
LITTLEDEVIL = Enemy("common", stcustomPath, 345912)
LITTLEDEVIL = Enemy("common", stcustomPath, 347491)
GREMLINS = Enemy("common", stcustomPath, 349070)
GREMLINS = Enemy("common", stcustomPath, 350649)
GREMLINS = Enemy("common", stcustomPath, 352228)
GREMLINS = Enemy("common", stcustomPath, 353807)
HARPY = Enemy("common", stcustomPath, 355386)
HARPY = Enemy("common", stcustomPath, 356965)
HARPY = Enemy("common", stcustomPath, 358544)
SEIREN = Enemy("common", stcustomPath, 382229)
ARMORNIGHT = Enemy("common", stcustomPath, 383808)
ARMORNIGHT = Enemy("common", stcustomPath, 385387)
ARMORNIGHT = Enemy("common", stcustomPath, 386966)
ARMORNIGHT = Enemy("common", stcustomPath, 388545)
ARMORNIGHT = Enemy("common", stcustomPath, 402756)
SWORDNIGHT = Enemy("common", stcustomPath, 415388)
SWORDNIGHT = Enemy("common", stcustomPath, 428020)
SWORDNIGHT = Enemy("common", stcustomPath, 429599)
DARKLORD = Enemy("common", stcustomPath, 431178)
DARKLORD = Enemy("common", stcustomPath, 432757)
NINJA = Enemy("common", stcustomPath, 434336)
NINJA = Enemy("common", stcustomPath, 435915)
NINJA = Enemy("common", stcustomPath, 437494)
NINJA = Enemy("common", stcustomPath, 439073)
NINJA = Enemy("common", stcustomPath, 442231)
NINJA = Enemy("common", stcustomPath, 443810)
NINJAMASTER = Enemy("common", stcustomPath, 445389)
NINJAMASTER = Enemy("common", stcustomPath, 446968)
NINJAMASTER = Enemy("common", stcustomPath, 448547)
NINJAMASTER = Enemy("common", stcustomPath, 461179)
NINJAMASTER = Enemy("common", stcustomPath, 462758)
KNIGHTBLADE = Enemy("common", stcustomPath, 464337)
KNIGHTBLADE = Enemy("common", stcustomPath, 465916)
EVILSWORD = Enemy("common", stcustomPath, 467495)
EVILSWORD = Enemy("common", stcustomPath, 470653)
ELEMENTSWORD = Enemy("common", stcustomPath, 472232)
ELEMENTSWORD = Enemy("common", stcustomPath, 473811)
SHAPESHIFTER = Enemy("common", stcustomPath, 475390)
SHAPESHIFTER = Enemy("common", stcustomPath, 476969)
SHAPESHIFTER = Enemy("common", stcustomPath, 478548)
SHADOWZERO = Enemy("common", stcustomPath, 480127)
SHADOWZERO = Enemy("common", stcustomPath, 481706)
SPECTRE = Enemy("common", stcustomPath, 502233)
SPECTRE = Enemy("common", stcustomPath, 503812)
SPECTRE = Enemy("common", stcustomPath, 505391)
SPECTRE = Enemy("common", stcustomPath, 506970)
GHOST = Enemy("common", stcustomPath, 508549)
GHOST = Enemy("common", stcustomPath, 510128)
GHOST = Enemy("common", stcustomPath, 511707)
GHOST = Enemy("common", stcustomPath, 513286)
DARKPRIEST = Enemy("common", stcustomPath, 514865)
DARKPRIEST = Enemy("common", stcustomPath, 516444)
DARKPRIEST = Enemy("common", stcustomPath, 518023)
DARKPRIEST = Enemy("common", stcustomPath, 519602)
DARKPRIEST = Enemy("common", stcustomPath, 521181)
DARKPRIEST = Enemy("common", stcustomPath, 522760)
DARKPRIEST = Enemy("common", stcustomPath, 535392)
EVILSHERMAN = Enemy("common", stcustomPath, 536971)
EVILSHERMAN = Enemy("common", stcustomPath, 538550)
EVILSHERMAN = Enemy("common", stcustomPath, 540129)
NECROMANCER = Enemy("common", stcustomPath, 541708)
NECROMANCER = Enemy("common", stcustomPath, 543287)
GRELL = Enemy("common", stcustomPath, 544866)
GRELL = Enemy("common", stcustomPath, 546445)
GRELL = Enemy("common", stcustomPath, 548024)
GRELLMAGE = Enemy("common", stcustomPath, 560656)
PAKKUNOTAMA = Enemy("common", stcustomPath, 562235)
PAKKUNOTAMA = Enemy("common", stcustomPath, 563814)
PAKKUNOTAMA = Enemy("common", stcustomPath, 565393)
PAKKURIOTAMA = Enemy("common", stcustomPath, 578025)
PAKKUNTOKAGE = Enemy("common", stcustomPath, 579604)
PAKKUNTOKAGE = Enemy("common", stcustomPath, 581183)
PAKKUNTOKAGE = Enemy("common", stcustomPath, 582762)
PAKKUNDRAGON = Enemy("common", stcustomPath, 595394)
POT = Enemy("common", stcustomPath, 596973)
POT = Enemy("common", stcustomPath, 598552)
POT = Enemy("common", stcustomPath, 600131)
MAMAPOT = Enemy("common", stcustomPath, 601710)
MAMAPOT = Enemy("common", stcustomPath, 603289)
MAMAPOT = Enemy("common", stcustomPath, 615921)
PAPAPOT = Enemy("common", stcustomPath, 628553)
PAPAPOT = Enemy("common", stcustomPath, 630132)
PAPAPOT = Enemy("common", stcustomPath, 631711)
SAHUAGIN = Enemy("common", stcustomPath, 633290)
SAHUAGIN = Enemy("common", stcustomPath, 634869)
SAHUAGIN = Enemy("common", stcustomPath, 647501)
PETITPOSEIDON = Enemy("common", stcustomPath, 660133)
SEASERPENT = Enemy("common", stcustomPath, 661712)
SEASERPENT = Enemy("common", stcustomPath, 663291)
SEADRAGON = Enemy("common", stcustomPath, 675923)
DUCKSOLDIER = Enemy("common", stcustomPath, 677502)
DUCKSOLDIER = Enemy("common", stcustomPath, 679081)
DUCKGENERAL = Enemy("common", stcustomPath, 691713)
BARETTE = Enemy("common", stcustomPath, 693292)
GOLDBARETTE = Enemy("common", stcustomPath, 694871)
GOLDBARETTE = Enemy("common", stcustomPath, 707503)
FIREDRAKE = Enemy("common", stcustomPath, 709082)
FIREDRAKE = Enemy("common", stcustomPath, 721714)
BASILISK = Enemy("common", stcustomPath, 723293)
BASILISK = Enemy("common", stcustomPath, 724872)
WEREWOLF = Enemy("common", stcustomPath, 728030)
WEREWOLF = Enemy("common", stcustomPath, 729609)
WEREWOLF = Enemy("common", stcustomPath, 731188)
BLACKFANG = Enemy("common", stcustomPath, 732767)
BLACKFANG = Enemy("common", stcustomPath, 734346)
BLACKFANG = Enemy("common", stcustomPath, 735925)
BLACKFANG = Enemy("common", stcustomPath, 737504)
SILVERWOLF = Enemy("common", stcustomPath, 739083)
SILVERWOLF = Enemy("common", stcustomPath, 751715)
SILVERWOLF = Enemy("common", stcustomPath, 753294)
BLOODYWOLF = Enemy("common", stcustomPath, 765926)
BLOODYWOLF = Enemy("common", stcustomPath, 767505)
BLOODYWOLF = Enemy("common", stcustomPath, 769084)
WOLFDEVIL = Enemy("common", stcustomPath, 770663)
WOLFDEVIL = Enemy("common", stcustomPath, 772242)
WOLFDEVIL = Enemy("common", stcustomPath, 773821)
MEGACRAWLER = Enemy("common", stcustomPath, 775400)
MEGACRAWLER = Enemy("common", stcustomPath, 776979)
GIGACRAWLER = Enemy("common", stcustomPath, 789611)
GIGACRAWLER = Enemy("common", stcustomPath, 791190)
PETITDRAGON = Enemy("common", stcustomPath, 803822)
FROSTDRAGON = Enemy("common", stcustomPath, 816454)
FROSTDRAGON = Enemy("common", stcustomPath, 818033)
PETITIAMATT = Enemy("common", stcustomPath, 819612)
PETITIAMATT = Enemy("common", stcustomPath, 821191)
PETITIAMATT = Enemy("common", stcustomPath, 822770)
PETIDRAZOMBIE = Enemy("common", stcustomPath, 824349)
PETIDRAZOMBIE = Enemy("common", stcustomPath, 825928)
CARMILLA = Enemy("common", stcustomPath, 838560)
CARMILLAQUEEN = Enemy("common", stcustomPath, 840139)
CARMILLAQUEEN = Enemy("common", stcustomPath, 841718)
CARMILLAQUEEN = Enemy("common", stcustomPath, 843297)
CARMILLAQUEEN = Enemy("common", stcustomPath, 844876)
BOULDER = Enemy("common", stcustomPath, 846455)
POWERBOULDER = Enemy("common", stcustomPath, 848034)
POWERBOULDER = Enemy("common", stcustomPath, 849613)
LESSERDAEMON = Enemy("common", stcustomPath, 851192)
LESSERDAEMON = Enemy("common", stcustomPath, 852771)
LESSERDAEMON = Enemy("common", stcustomPath, 854350)
GREATDAEMON = Enemy("common", stcustomPath, 855929)
GREATDAEMON = Enemy("common", stcustomPath, 857508)
GREATDAEMON = Enemy("common", stcustomPath, 859087)
GREATDAEMON = Enemy("common", stcustomPath, 860666)
GREATDAEMON = Enemy("common", stcustomPath, 862245)
OGREBOX = Enemy("common", stcustomPath, 863824)
OGREBOX = Enemy("common", stcustomPath, 865403)
OGREBOX = Enemy("common", stcustomPath, 866982)
OGREBOX = Enemy("common", stcustomPath, 868561)
KAISERMIMIC = Enemy("common", stcustomPath, 870140)
GREATDAEMON = Enemy("common", stcustomPath, 871719)
KERBEROS = Enemy("common", stcustomPath, 873298)
GOLDBARETTE = Enemy("common", stcustomPath, 874877)
LITTLEDEVIL = Enemy("common", stcustomPath, 876456)
PETITDRAGON = Enemy("common", stcustomPath, 878035)
SHAPESHIFTER = Enemy("common", stcustomPath, 879614)
SHADOWZERO = Enemy("common", stcustomPath, 881193)
RABI = Enemy("common", stcustomPath, 882772)
RABIRION = Enemy("common", stcustomPath, 884351)
KINGRABI = Enemy("common", stcustomPath, 885930)
GREATRABI = Enemy("common", stcustomPath, 887509)
KAISERMIMIC = Enemy("common", stcustomPath, 889088)
HARPY = Enemy("common", stcustomPath, 890667)
RABI = Enemy("common", stcustomPath, 892246)
KARL = Enemy("common", stcustomPath, 893825)
EAGLE = Enemy("common", stcustomPath, 895404)
Bruiser = Enemy("common", stcustomPath, 896983)
GOBLIN = Enemy("common", stcustomPath, 898562)
RABI = Enemy("common", stcustomPath, 900141)
GUARDIAN = Enemy("common", stcustomPath, 901720)
GREMLINS = Enemy("common", stcustomPath, 903299)
KNIGHTBLADE = Enemy("common", stcustomPath, 904878)
LESSERDAEMON = Enemy("common", stcustomPath, 906457)
RASTERBUG = Enemy("common", stcustomPath, 908036)
KERBEROS = Enemy("common", stcustomPath, 909615)
HIGHWIZARD = Enemy("common", stcustomPath, 911194)
DEATHMACHINE = Enemy("common", stcustomPath, 912773)
DARKLORD = Enemy("common", stcustomPath, 914352)
PETITIAMATT = Enemy("common", stcustomPath, 915931)
GREATDAEMON = Enemy("common", stcustomPath, 917510)
RASTERBUG = Enemy("common", stcustomPath, 919089)
SLIMEPRINCE = Enemy("common", stcustomPath, 920668)
NIDORION = Enemy("common", stcustomPath, 922247)
QUEENBEE = Enemy("common", stcustomPath, 923826)
BASILISK = Enemy("common", stcustomPath, 925405)
GIGACRAWLER = Enemy("common", stcustomPath, 926984)
COCKATRICE = Enemy("common", stcustomPath, 928563)
BIRD = Enemy("common", stcustomPath, 930142)
WIZARD = Enemy("common", stcustomPath, 931721)
HIGHWIZARD = Enemy("common", stcustomPath, 933300)
SWORDNIGHT = Enemy("common", stcustomPath, 934879)
DARKLORD = Enemy("common", stcustomPath, 936458)
NINJAMASTER = Enemy("common", stcustomPath, 938037)
KNIGHTBLADE = Enemy("common", stcustomPath, 939616)
EVILSHERMAN = Enemy("common", stcustomPath, 941195)
DUCKGENERAL = Enemy("common", stcustomPath, 942774)
GOLDBARETTE = Enemy("common", stcustomPath, 944353)
GREATDAEMON = Enemy("common", stcustomPath, 945932)
SHAPESHIFTER = Enemy("common", stcustomPath, 947511)
COCKATRICE = Enemy("common", stcustomPath, 949090)
BIRD = Enemy("common", stcustomPath, 950669)
LITTLEDEVIL = Enemy("common", stcustomPath, 952248)
GREMLINS = Enemy("common", stcustomPath, 953827)
NINJA = Enemy("common", stcustomPath, 955406)
NINJAMASTER = Enemy("common", stcustomPath, 956985)
KNIGHTBLADE = Enemy("common", stcustomPath, 958564)
EVILSHERMAN = Enemy("common", stcustomPath, 960143)
DUCKGENERAL = Enemy("common", stcustomPath, 961722)
GOLDBARETTE = Enemy("common", stcustomPath, 963301)
GREATDAEMON = Enemy("common", stcustomPath, 964880)
SHAPESHIFTER = Enemy("common", stcustomPath, 966459)
ZOMBIE = Enemy("common", stcustomPath, 968038)
GHOUL = Enemy("common", stcustomPath, 969617)
GHOST = Enemy("common", stcustomPath, 971196)
NECROMANCER = Enemy("common", stcustomPath, 972775)
PETIDRAZOMBIE = Enemy("common", stcustomPath, 974354)
ZOMBIE = Enemy("common", stcustomPath, 975933)
GHOUL = Enemy("common", stcustomPath, 977512)
SLIMEPRINCE = Enemy("common", stcustomPath, 979091)
GHOST = Enemy("common", stcustomPath, 980670)
NECROMANCER = Enemy("common", stcustomPath, 982249)
GRELLMAGE = Enemy("common", stcustomPath, 983828)
PAKKURIOTAMA = Enemy("common", stcustomPath, 985407)
PAKKUNDRAGON = Enemy("common", stcustomPath, 986986)
PETIDRAZOMBIE = Enemy("common", stcustomPath, 988565)
POWERBOULDER = Enemy("common", stcustomPath, 990144)
KAISERMIMIC = Enemy("common", stcustomPath, 991723)
UNICORNHEAD = Enemy("common", stcustomPath, 993302)
GOLDUNICO = Enemy("common", stcustomPath, 994881)
HIGHWIZARD = Enemy("common", stcustomPath, 996460)
GUARDIAN = Enemy("common", stcustomPath, 998039)
DEATHMACHINE = Enemy("common", stcustomPath, 999618)
PAPAPOT = Enemy("common", stcustomPath, 1001197)
PETITPOSEIDON = Enemy("common", stcustomPath, 1002776)
SAHUAGIN = Enemy("common", stcustomPath, 1004355)
SEADRAGON = Enemy("common", stcustomPath, 1005934)
FROSTDRAGON = Enemy("common", stcustomPath, 1007513)
KAISERMIMIC = Enemy("common", stcustomPath, 1009092)
UNICORNHEAD = Enemy("common", stcustomPath, 1010671)
GOLDUNICO = Enemy("common", stcustomPath, 1012250)
HIGHWIZARD = Enemy("common", stcustomPath, 1013829)
GUARDIAN = Enemy("common", stcustomPath, 1015408)
DEATHMACHINE = Enemy("common", stcustomPath, 1016987)
PAPAPOT = Enemy("common", stcustomPath, 1018566)
SAHUAGIN = Enemy("common", stcustomPath, 1020145)
PETITPOSEIDON = Enemy("common", stcustomPath, 1021724)
SEADRAGON = Enemy("common", stcustomPath, 1023303)
FROSTDRAGON = Enemy("common", stcustomPath, 1024882)
SHADOWZERO = Enemy("common", stcustomPath, 1026461)
DARKBATTOM = Enemy("common", stcustomPath, 1028040)
BIRD = Enemy("common", stcustomPath, 1029619)
GREMLINS = Enemy("common", stcustomPath, 1031198)
SEIREN = Enemy("common", stcustomPath, 1032777)
ELEMENTSWORD = Enemy("common", stcustomPath, 1034356)
GIGACRAWLER = Enemy("common", stcustomPath, 1035935)
CARMILLAQUEEN = Enemy("common", stcustomPath, 1037514)
POWERBOULDER = Enemy("common", stcustomPath, 1039093)
LESSERDAEMON = Enemy("common", stcustomPath, 1040672)
GREATDAEMON = Enemy("common", stcustomPath, 1042251)
RABI = Enemy("common", stcustomPath, 1043830)
RABIRION = Enemy("common", stcustomPath, 1045409)
KINGRABI = Enemy("common", stcustomPath, 1046988)
GREATRABI = Enemy("common", stcustomPath, 1048567)
KAISERMIMIC = Enemy("common", stcustomPath, 1050146)
SAHAGIN = Enemy("common", stcustomPath, 1051725)


# ****** EnemyStatusStgodstcustom - *****

stgodstcustomPath = r'Game Files\uexp files\Orig\GodEnemyCustomStatusTable.uexp'

DARTHMATANGO_Lv38 = Enemy("common", stgodstcustomPath, 1690)
DARTHMATANGO_Lv40 = Enemy("common", stgodstcustomPath, 3269)
DARTHMATANGO_Lv42 = Enemy("common", stgodstcustomPath, 4848)
DARTHMATANGO_Lv44 = Enemy("common", stgodstcustomPath, 6427)
DARTHMATANGO_Lv46 = Enemy("common", stgodstcustomPath, 8006)
DARTHMATANGO_Lv48 = Enemy("common", stgodstcustomPath, 9585)
DARTHMATANGO_Lv50 = Enemy("common", stgodstcustomPath, 11164)
BEASTMASTER_Lv38 = Enemy("common", stgodstcustomPath, 12743)
BEASTMASTER_Lv40 = Enemy("common", stgodstcustomPath, 14322)
BEASTMASTER_Lv42 = Enemy("common", stgodstcustomPath, 15901)
BEASTMASTER_Lv44 = Enemy("common", stgodstcustomPath, 17480)
BEASTMASTER_Lv46 = Enemy("common", stgodstcustomPath, 19059)
BEASTMASTER_Lv48 = Enemy("common", stgodstcustomPath, 20638)
BEASTMASTER_Lv50 = Enemy("common", stgodstcustomPath, 22217)
SUMMON_KERBEROS_Lv38 = Enemy("common", stgodstcustomPath, 23796)
SUMMON_KERBEROS_Lv40 = Enemy("common", stgodstcustomPath, 25375)
SUMMON_KERBEROS_Lv42 = Enemy("common", stgodstcustomPath, 26954)
SUMMON_KERBEROS_Lv44 = Enemy("common", stgodstcustomPath, 28533)
SUMMON_KERBEROS_Lv46 = Enemy("common", stgodstcustomPath, 30112)
SUMMON_KERBEROS_Lv48 = Enemy("common", stgodstcustomPath, 31691)
SUMMON_KERBEROS_Lv50 = Enemy("common", stgodstcustomPath, 33270)
POROBINLEADER_Lv38 = Enemy("common", stgodstcustomPath, 34849)
POROBINLEADER_Lv40 = Enemy("common", stgodstcustomPath, 36428)
POROBINLEADER_Lv42 = Enemy("common", stgodstcustomPath, 38007)
POROBINLEADER_Lv44 = Enemy("common", stgodstcustomPath, 39586)
POROBINLEADER_Lv46 = Enemy("common", stgodstcustomPath, 41165)
POROBINLEADER_Lv48 = Enemy("common", stgodstcustomPath, 42744)
POROBINLEADER_Lv50 = Enemy("common", stgodstcustomPath, 44323)
GHOUL_Lv38 = Enemy("common", stgodstcustomPath, 45902)
GHOUL_Lv40 = Enemy("common", stgodstcustomPath, 47481)
GHOUL_Lv42 = Enemy("common", stgodstcustomPath, 49060)
GHOUL_Lv44 = Enemy("common", stgodstcustomPath, 50639)
GHOUL_Lv46 = Enemy("common", stgodstcustomPath, 52218)
GHOUL_Lv48 = Enemy("common", stgodstcustomPath, 53797)
GHOUL_Lv50 = Enemy("common", stgodstcustomPath, 55376)
SLIMEPRINCE_Lv38 = Enemy("common", stgodstcustomPath, 56955)
SLIMEPRINCE_Lv40 = Enemy("common", stgodstcustomPath, 58534)
SLIMEPRINCE_Lv42 = Enemy("common", stgodstcustomPath, 60113)
SLIMEPRINCE_Lv44 = Enemy("common", stgodstcustomPath, 61692)
SLIMEPRINCE_Lv46 = Enemy("common", stgodstcustomPath, 63271)
SLIMEPRINCE_Lv48 = Enemy("common", stgodstcustomPath, 64850)
SLIMEPRINCE_Lv50 = Enemy("common", stgodstcustomPath, 66429)
NIDORION_Lv38 = Enemy("common", stgodstcustomPath, 68008)
NIDORION_Lv40 = Enemy("common", stgodstcustomPath, 69587)
NIDORION_Lv42 = Enemy("common", stgodstcustomPath, 71166)
NIDORION_Lv44 = Enemy("common", stgodstcustomPath, 72745)
NIDORION_Lv46 = Enemy("common", stgodstcustomPath, 74324)
NIDORION_Lv48 = Enemy("common", stgodstcustomPath, 75903)
NIDORION_Lv50 = Enemy("common", stgodstcustomPath, 77482)
QUEENBEE_Lv38 = Enemy("common", stgodstcustomPath, 79061)
QUEENBEE_Lv40 = Enemy("common", stgodstcustomPath, 80640)
QUEENBEE_Lv42 = Enemy("common", stgodstcustomPath, 82219)
QUEENBEE_Lv44 = Enemy("common", stgodstcustomPath, 83798)
QUEENBEE_Lv46 = Enemy("common", stgodstcustomPath, 85377)
QUEENBEE_Lv48 = Enemy("common", stgodstcustomPath, 86956)
QUEENBEE_Lv50 = Enemy("common", stgodstcustomPath, 88535)
COCKATRICE_Lv38 = Enemy("common", stgodstcustomPath, 90114)
COCKATRICE_Lv40 = Enemy("common", stgodstcustomPath, 91693)
COCKATRICE_Lv42 = Enemy("common", stgodstcustomPath, 93272)
COCKATRICE_Lv44 = Enemy("common", stgodstcustomPath, 94851)
COCKATRICE_Lv46 = Enemy("common", stgodstcustomPath, 96430)
COCKATRICE_Lv48 = Enemy("common", stgodstcustomPath, 98009)
COCKATRICE_Lv50 = Enemy("common", stgodstcustomPath, 99588)
NEEDLEBIRD_Lv38 = Enemy("common", stgodstcustomPath, 101167)
NEEDLEBIRD_Lv40 = Enemy("common", stgodstcustomPath, 102746)
NEEDLEBIRD_Lv42 = Enemy("common", stgodstcustomPath, 104325)
NEEDLEBIRD_Lv44 = Enemy("common", stgodstcustomPath, 105904)
NEEDLEBIRD_Lv46 = Enemy("common", stgodstcustomPath, 107483)
NEEDLEBIRD_Lv48 = Enemy("common", stgodstcustomPath, 109062)
NEEDLEBIRD_Lv50 = Enemy("common", stgodstcustomPath, 110641)
COCKATBIRD_Lv38 = Enemy("common", stgodstcustomPath, 112220)
COCKATBIRD_Lv40 = Enemy("common", stgodstcustomPath, 113799)
COCKATBIRD_Lv42 = Enemy("common", stgodstcustomPath, 115378)
COCKATBIRD_Lv44 = Enemy("common", stgodstcustomPath, 116957)
COCKATBIRD_Lv46 = Enemy("common", stgodstcustomPath, 118536)
COCKATBIRD_Lv48 = Enemy("common", stgodstcustomPath, 120115)
COCKATBIRD_Lv50 = Enemy("common", stgodstcustomPath, 121694)
LITTLEDEVIL_Lv38 = Enemy("common", stgodstcustomPath, 123273)
LITTLEDEVIL_Lv40 = Enemy("common", stgodstcustomPath, 124852)
LITTLEDEVIL_Lv42 = Enemy("common", stgodstcustomPath, 126431)
LITTLEDEVIL_Lv44 = Enemy("common", stgodstcustomPath, 128010)
LITTLEDEVIL_Lv46 = Enemy("common", stgodstcustomPath, 129589)
LITTLEDEVIL_Lv48 = Enemy("common", stgodstcustomPath, 131168)
LITTLEDEVIL_Lv50 = Enemy("common", stgodstcustomPath, 132747)
UNUSED_HARPY_Lv38 = Enemy("common", stgodstcustomPath, 134326)
UNUSED_HARPY_Lv40 = Enemy("common", stgodstcustomPath, 135905)
UNUSED_HARPY_Lv42 = Enemy("common", stgodstcustomPath, 137484)
UNUSED_HARPY_Lv44 = Enemy("common", stgodstcustomPath, 139063)
UNUSED_HARPY_Lv46 = Enemy("common", stgodstcustomPath, 140642)
UNUSED_HARPY_Lv48 = Enemy("common", stgodstcustomPath, 142221)
UNUSED_HARPY_Lv50 = Enemy("common", stgodstcustomPath, 143800)
SEIREN_Lv38 = Enemy("common", stgodstcustomPath, 145379)
SEIREN_Lv40 = Enemy("common", stgodstcustomPath, 146958)
SEIREN_Lv42 = Enemy("common", stgodstcustomPath, 148537)
SEIREN_Lv44 = Enemy("common", stgodstcustomPath, 150116)
SEIREN_Lv46 = Enemy("common", stgodstcustomPath, 151695)
SEIREN_Lv48 = Enemy("common", stgodstcustomPath, 153274)
SEIREN_Lv50 = Enemy("common", stgodstcustomPath, 154853)
UNUSED_ARMORNIGHT_Lv38 = Enemy("common", stgodstcustomPath, 156432)
UNUSED_ARMORNIGHT_Lv40 = Enemy("common", stgodstcustomPath, 158011)
UNUSED_ARMORNIGHT_Lv42 = Enemy("common", stgodstcustomPath, 159590)
UNUSED_ARMORNIGHT_Lv44 = Enemy("common", stgodstcustomPath, 161169)
UNUSED_ARMORNIGHT_Lv46 = Enemy("common", stgodstcustomPath, 162748)
UNUSED_ARMORNIGHT_Lv48 = Enemy("common", stgodstcustomPath, 164327)
UNUSED_ARMORNIGHT_Lv50 = Enemy("common", stgodstcustomPath, 165906)
SILVERNIGHT_Lv38 = Enemy("common", stgodstcustomPath, 167485)
SILVERNIGHT_Lv40 = Enemy("common", stgodstcustomPath, 169064)
SILVERNIGHT_Lv42 = Enemy("common", stgodstcustomPath, 170643)
SILVERNIGHT_Lv44 = Enemy("common", stgodstcustomPath, 172222)
SILVERNIGHT_Lv46 = Enemy("common", stgodstcustomPath, 173801)
SILVERNIGHT_Lv48 = Enemy("common", stgodstcustomPath, 175380)
SILVERNIGHT_Lv50 = Enemy("common", stgodstcustomPath, 176959)
SWORDNIGHT_Lv38 = Enemy("common", stgodstcustomPath, 178538)
SWORDNIGHT_Lv40 = Enemy("common", stgodstcustomPath, 180117)
SWORDNIGHT_Lv42 = Enemy("common", stgodstcustomPath, 181696)
SWORDNIGHT_Lv44 = Enemy("common", stgodstcustomPath, 183275)
SWORDNIGHT_Lv46 = Enemy("common", stgodstcustomPath, 184854)
SWORDNIGHT_Lv48 = Enemy("common", stgodstcustomPath, 186433)
SWORDNIGHT_Lv50 = Enemy("common", stgodstcustomPath, 188012)
NINJAMASTER_Lv38 = Enemy("common", stgodstcustomPath, 189591)
NINJAMASTER_Lv40 = Enemy("common", stgodstcustomPath, 191170)
NINJAMASTER_Lv42 = Enemy("common", stgodstcustomPath, 192749)
NINJAMASTER_Lv44 = Enemy("common", stgodstcustomPath, 194328)
NINJAMASTER_Lv46 = Enemy("common", stgodstcustomPath, 195907)
NINJAMASTER_Lv48 = Enemy("common", stgodstcustomPath, 197486)
NINJAMASTER_Lv50 = Enemy("common", stgodstcustomPath, 199065)
DARKPRIEST_Lv38 = Enemy("common", stgodstcustomPath, 200644)
DARKPRIEST_Lv40 = Enemy("common", stgodstcustomPath, 202223)
DARKPRIEST_Lv42 = Enemy("common", stgodstcustomPath, 203802)
DARKPRIEST_Lv44 = Enemy("common", stgodstcustomPath, 205381)
DARKPRIEST_Lv46 = Enemy("common", stgodstcustomPath, 206960)
DARKPRIEST_Lv48 = Enemy("common", stgodstcustomPath, 208539)
DARKPRIEST_Lv50 = Enemy("common", stgodstcustomPath, 210118)
GRELLMAGE_Lv38 = Enemy("common", stgodstcustomPath, 211697)
GRELLMAGE_Lv40 = Enemy("common", stgodstcustomPath, 213276)
GRELLMAGE_Lv42 = Enemy("common", stgodstcustomPath, 214855)
GRELLMAGE_Lv44 = Enemy("common", stgodstcustomPath, 216434)
GRELLMAGE_Lv46 = Enemy("common", stgodstcustomPath, 218013)
GRELLMAGE_Lv48 = Enemy("common", stgodstcustomPath, 219592)
GRELLMAGE_Lv50 = Enemy("common", stgodstcustomPath, 221171)
PAKKURIOTAMA_Lv38 = Enemy("common", stgodstcustomPath, 222750)
PAKKURIOTAMA_Lv40 = Enemy("common", stgodstcustomPath, 224329)
PAKKURIOTAMA_Lv42 = Enemy("common", stgodstcustomPath, 225908)
PAKKURIOTAMA_Lv44 = Enemy("common", stgodstcustomPath, 227487)
PAKKURIOTAMA_Lv46 = Enemy("common", stgodstcustomPath, 229066)
PAKKURIOTAMA_Lv48 = Enemy("common", stgodstcustomPath, 230645)
PAKKURIOTAMA_Lv50 = Enemy("common", stgodstcustomPath, 232224)
PAKKUNDRAGON_Lv38 = Enemy("common", stgodstcustomPath, 233803)
PAKKUNDRAGON_Lv40 = Enemy("common", stgodstcustomPath, 235382)
PAKKUNDRAGON_Lv42 = Enemy("common", stgodstcustomPath, 236961)
PAKKUNDRAGON_Lv44 = Enemy("common", stgodstcustomPath, 238540)
PAKKUNDRAGON_Lv46 = Enemy("common", stgodstcustomPath, 240119)
PAKKUNDRAGON_Lv48 = Enemy("common", stgodstcustomPath, 241698)
PAKKUNDRAGON_Lv50 = Enemy("common", stgodstcustomPath, 243277)
MAMAPOT_Lv38 = Enemy("common", stgodstcustomPath, 244856)
MAMAPOT_Lv40 = Enemy("common", stgodstcustomPath, 246435)
MAMAPOT_Lv42 = Enemy("common", stgodstcustomPath, 248014)
MAMAPOT_Lv44 = Enemy("common", stgodstcustomPath, 249593)
MAMAPOT_Lv46 = Enemy("common", stgodstcustomPath, 251172)
MAMAPOT_Lv48 = Enemy("common", stgodstcustomPath, 252751)
MAMAPOT_Lv50 = Enemy("common", stgodstcustomPath, 254330)
SUMMON_PAPAPOT_Lv38 = Enemy("common", stgodstcustomPath, 255909)
SUMMON_PAPAPOT_Lv40 = Enemy("common", stgodstcustomPath, 257488)
SUMMON_PAPAPOT_Lv42 = Enemy("common", stgodstcustomPath, 259067)
SUMMON_PAPAPOT_Lv44 = Enemy("common", stgodstcustomPath, 260646)
SUMMON_PAPAPOT_Lv46 = Enemy("common", stgodstcustomPath, 262225)
SUMMON_PAPAPOT_Lv48 = Enemy("common", stgodstcustomPath, 263804)
SUMMON_PAPAPOT_Lv50 = Enemy("common", stgodstcustomPath, 265383)
SUMMON_SAHUAGIN_Lv38 = Enemy("common", stgodstcustomPath, 266962)
SUMMON_SAHUAGIN_Lv40 = Enemy("common", stgodstcustomPath, 268541)
SUMMON_SAHUAGIN_Lv42 = Enemy("common", stgodstcustomPath, 270120)
SUMMON_SAHUAGIN_Lv44 = Enemy("common", stgodstcustomPath, 271699)
SUMMON_SAHUAGIN_Lv46 = Enemy("common", stgodstcustomPath, 273278)
SUMMON_SAHUAGIN_Lv48 = Enemy("common", stgodstcustomPath, 274857)
SUMMON_SAHUAGIN_Lv50 = Enemy("common", stgodstcustomPath, 276436)
PETITPOSEIDON_Lv38 = Enemy("common", stgodstcustomPath, 278015)
PETITPOSEIDON_Lv40 = Enemy("common", stgodstcustomPath, 279594)
PETITPOSEIDON_Lv42 = Enemy("common", stgodstcustomPath, 281173)
PETITPOSEIDON_Lv44 = Enemy("common", stgodstcustomPath, 282752)
PETITPOSEIDON_Lv46 = Enemy("common", stgodstcustomPath, 284331)
PETITPOSEIDON_Lv48 = Enemy("common", stgodstcustomPath, 285910)
PETITPOSEIDON_Lv50 = Enemy("common", stgodstcustomPath, 287489)
SEADRAGON_Lv38 = Enemy("common", stgodstcustomPath, 289068)
SEADRAGON_Lv40 = Enemy("common", stgodstcustomPath, 290647)
SEADRAGON_Lv42 = Enemy("common", stgodstcustomPath, 292226)
SEADRAGON_Lv44 = Enemy("common", stgodstcustomPath, 293805)
SEADRAGON_Lv46 = Enemy("common", stgodstcustomPath, 295384)
SEADRAGON_Lv48 = Enemy("common", stgodstcustomPath, 296963)
SEADRAGON_Lv50 = Enemy("common", stgodstcustomPath, 298542)
DUCKGENERAL_Lv38 = Enemy("common", stgodstcustomPath, 300121)
DUCKGENERAL_Lv40 = Enemy("common", stgodstcustomPath, 301700)
DUCKGENERAL_Lv42 = Enemy("common", stgodstcustomPath, 303279)
DUCKGENERAL_Lv44 = Enemy("common", stgodstcustomPath, 304858)
DUCKGENERAL_Lv46 = Enemy("common", stgodstcustomPath, 306437)
DUCKGENERAL_Lv48 = Enemy("common", stgodstcustomPath, 308016)
DUCKGENERAL_Lv50 = Enemy("common", stgodstcustomPath, 309595)
SUMMON_GOLDBARETTE_Lv38 = Enemy("common", stgodstcustomPath, 311174)
SUMMON_GOLDBARETTE_Lv40 = Enemy("common", stgodstcustomPath, 312753)
SUMMON_GOLDBARETTE_Lv42 = Enemy("common", stgodstcustomPath, 314332)
SUMMON_GOLDBARETTE_Lv44 = Enemy("common", stgodstcustomPath, 315911)
SUMMON_GOLDBARETTE_Lv46 = Enemy("common", stgodstcustomPath, 317490)
SUMMON_GOLDBARETTE_Lv48 = Enemy("common", stgodstcustomPath, 319069)
SUMMON_GOLDBARETTE_Lv50 = Enemy("common", stgodstcustomPath, 320648)
FIREDRAKE_Lv38 = Enemy("common", stgodstcustomPath, 322227)
FIREDRAKE_Lv40 = Enemy("common", stgodstcustomPath, 323806)
FIREDRAKE_Lv42 = Enemy("common", stgodstcustomPath, 325385)
FIREDRAKE_Lv44 = Enemy("common", stgodstcustomPath, 326964)
FIREDRAKE_Lv46 = Enemy("common", stgodstcustomPath, 328543)
FIREDRAKE_Lv48 = Enemy("common", stgodstcustomPath, 330122)
FIREDRAKE_Lv50 = Enemy("common", stgodstcustomPath, 331701)
SILVERWOLF_Lv38 = Enemy("common", stgodstcustomPath, 333280)
SILVERWOLF_Lv40 = Enemy("common", stgodstcustomPath, 334859)
SILVERWOLF_Lv42 = Enemy("common", stgodstcustomPath, 336438)
SILVERWOLF_Lv44 = Enemy("common", stgodstcustomPath, 338017)
SILVERWOLF_Lv46 = Enemy("common", stgodstcustomPath, 339596)
SILVERWOLF_Lv48 = Enemy("common", stgodstcustomPath, 341175)
SILVERWOLF_Lv50 = Enemy("common", stgodstcustomPath, 342754)
BLOODYWOLF_Lv38 = Enemy("common", stgodstcustomPath, 344333)
BLOODYWOLF_Lv40 = Enemy("common", stgodstcustomPath, 345912)
BLOODYWOLF_Lv42 = Enemy("common", stgodstcustomPath, 347491)
BLOODYWOLF_Lv44 = Enemy("common", stgodstcustomPath, 349070)
BLOODYWOLF_Lv46 = Enemy("common", stgodstcustomPath, 350649)
BLOODYWOLF_Lv48 = Enemy("common", stgodstcustomPath, 352228)
BLOODYWOLF_Lv50 = Enemy("common", stgodstcustomPath, 353807)
GIGACRAWLER_Lv38 = Enemy("common", stgodstcustomPath, 355386)
GIGACRAWLER_Lv40 = Enemy("common", stgodstcustomPath, 356965)
GIGACRAWLER_Lv42 = Enemy("common", stgodstcustomPath, 358544)
GIGACRAWLER_Lv44 = Enemy("common", stgodstcustomPath, 360123)
GIGACRAWLER_Lv46 = Enemy("common", stgodstcustomPath, 361702)
GIGACRAWLER_Lv48 = Enemy("common", stgodstcustomPath, 363281)
GIGACRAWLER_Lv50 = Enemy("common", stgodstcustomPath, 364860)
PETITDRAGON_Lv38 = Enemy("common", stgodstcustomPath, 366439)
PETITDRAGON_Lv40 = Enemy("common", stgodstcustomPath, 368018)
PETITDRAGON_Lv42 = Enemy("common", stgodstcustomPath, 369597)
PETITDRAGON_Lv44 = Enemy("common", stgodstcustomPath, 371176)
PETITDRAGON_Lv46 = Enemy("common", stgodstcustomPath, 372755)
PETITDRAGON_Lv48 = Enemy("common", stgodstcustomPath, 374334)
PETITDRAGON_Lv50 = Enemy("common", stgodstcustomPath, 375913)
FROSTDRAGON_Lv38 = Enemy("common", stgodstcustomPath, 377492)
FROSTDRAGON_Lv40 = Enemy("common", stgodstcustomPath, 379071)
FROSTDRAGON_Lv42 = Enemy("common", stgodstcustomPath, 380650)
FROSTDRAGON_Lv44 = Enemy("common", stgodstcustomPath, 382229)
FROSTDRAGON_Lv46 = Enemy("common", stgodstcustomPath, 383808)
FROSTDRAGON_Lv48 = Enemy("common", stgodstcustomPath, 385387)
FROSTDRAGON_Lv50 = Enemy("common", stgodstcustomPath, 386966)
CARMILLA_Lv38 = Enemy("common", stgodstcustomPath, 388545)
CARMILLA_Lv40 = Enemy("common", stgodstcustomPath, 390124)
CARMILLA_Lv42 = Enemy("common", stgodstcustomPath, 391703)
CARMILLA_Lv44 = Enemy("common", stgodstcustomPath, 393282)
CARMILLA_Lv46 = Enemy("common", stgodstcustomPath, 394861)
CARMILLA_Lv48 = Enemy("common", stgodstcustomPath, 396440)
CARMILLA_Lv50 = Enemy("common", stgodstcustomPath, 398019)
OGREBOX_Lv38 = Enemy("common", stgodstcustomPath, 399598)
OGREBOX_Lv40 = Enemy("common", stgodstcustomPath, 401177)
OGREBOX_Lv42 = Enemy("common", stgodstcustomPath, 402756)
OGREBOX_Lv44 = Enemy("common", stgodstcustomPath, 404335)
OGREBOX_Lv46 = Enemy("common", stgodstcustomPath, 405914)
OGREBOX_Lv48 = Enemy("common", stgodstcustomPath, 407493)
OGREBOX_Lv50 = Enemy("common", stgodstcustomPath, 409072)


# ********** Files in ...\Data\Csv\CharaData **********

# ****** EnemyStatusStEnStat - *****

stEnStatPath = r'Game Files\uexp files\Orig\EnemyStatusTable.uexp'

RABI = Enemy("common", stEnStatPath, 111)
RABIRION = Enemy("common", stEnStatPath, 1690)
KINGRABI = Enemy("common", stEnStatPath, 3269)
GREATRABI = Enemy("common", stEnStatPath, 4848)
MAIKONIDO = Enemy("common", stEnStatPath, 6427)
DARTHMATANGO = Enemy("common", stEnStatPath, 8006)
BATTOM = Enemy("common", stEnStatPath, 9585)
DARKBATTOM = Enemy("common", stEnStatPath, 11164)
GOBLIN = Enemy("common", stEnStatPath, 12743)
GOBLINLORD = Enemy("common", stEnStatPath, 14322)
BEASTMASTER = Enemy("common", stEnStatPath, 15901)
BOUNDWOLF = Enemy("common", stEnStatPath, 17480)
KERBEROS = Enemy("common", stEnStatPath, 19059)
ASSASSINBUG = Enemy("common", stEnStatPath, 20638)
RASTERBUG = Enemy("common", stEnStatPath, 22217)
PORON = Enemy("common", stEnStatPath, 23796)
POROBINHOOD = Enemy("common", stEnStatPath, 25375)
POROBINLEADER = Enemy("common", stEnStatPath, 26954)
ZOMBIE = Enemy("common", stEnStatPath, 28533)
GHOUL = Enemy("common", stEnStatPath, 30112)
SLIME = Enemy("common", stEnStatPath, 31691)
SLIMEPRINCE = Enemy("common", stEnStatPath, 33270)
MALLBEAR = Enemy("common", stEnStatPath, 34849)
NIDORION = Enemy("common", stEnStatPath, 36428)
GALBEE = Enemy("common", stEnStatPath, 38007)
LADYBEE = Enemy("common", stEnStatPath, 39586)
QUEENBEE = Enemy("common", stEnStatPath, 41165)
UNICORNHEAD = Enemy("common", stEnStatPath, 42744)
GOLDUNICO = Enemy("common", stEnStatPath, 44323)
MAGICIAN = Enemy("common", stEnStatPath, 45902)
WIZARD = Enemy("common", stEnStatPath, 47481)
HIGHWIZARD = Enemy("common", stEnStatPath, 49060)
MACHINEGOLEM = Enemy("common", stEnStatPath, 50639)
GUARDIAN = Enemy("common", stEnStatPath, 52218)
DEATHMACHINE = Enemy("common", stEnStatPath, 53797)
COCKATRICE = Enemy("common", stEnStatPath, 55376)
NEEDLEBIRD = Enemy("common", stEnStatPath, 56955)
BIRD = Enemy("common", stEnStatPath, 58534)
LITTLEDEVIL = Enemy("common", stEnStatPath, 60113)
GREMLINS = Enemy("common", stEnStatPath, 61692)
HARPY = Enemy("common", stEnStatPath, 63271)
SEIREN = Enemy("common", stEnStatPath, 64850)
ARMORNIGHT = Enemy("common", stEnStatPath, 66429)
SILVERNIGHT = Enemy("common", stEnStatPath, 68008)
SWORDNIGHT = Enemy("common", stEnStatPath, 69587)
DARKLORD = Enemy("common", stEnStatPath, 71166)
NINJA = Enemy("common", stEnStatPath, 72745)
NINJAMASTER = Enemy("common", stEnStatPath, 74324)
KNIGHTBLADE = Enemy("common", stEnStatPath, 75903)
EVILSWORD = Enemy("common", stEnStatPath, 77482)
ELEMENTSWORD = Enemy("common", stEnStatPath, 79061)
SHAPESHIFTER = Enemy("common", stEnStatPath, 80640)
SHADOWZERO = Enemy("common", stEnStatPath, 82219)
SPECTRE = Enemy("common", stEnStatPath, 93272)
GHOST = Enemy("common", stEnStatPath, 94851)
DARKPRIEST = Enemy("common", stEnStatPath, 96430)
EVILSHERMAN = Enemy("common", stEnStatPath, 98009)
NECROMANCER = Enemy("common", stEnStatPath, 99588)
GRELL = Enemy("common", stEnStatPath, 101167)
GRELLMAGE = Enemy("common", stEnStatPath, 102746)
PAKKUNOTAMA = Enemy("common", stEnStatPath, 104325)
PAKKURIOTAMA = Enemy("common", stEnStatPath, 105904)
PAKKUNTOKAGE = Enemy("common", stEnStatPath, 107483)
PAKKUNDRAGON = Enemy("common", stEnStatPath, 109062)
POT = Enemy("common", stEnStatPath, 110641)
MAMAPOT = Enemy("common", stEnStatPath, 112220)
PAPAPOT = Enemy("common", stEnStatPath, 113799)
SAHUAGIN = Enemy("common", stEnStatPath, 115378)
PETITPOSEIDON = Enemy("common", stEnStatPath, 116957)
SEASERPENT = Enemy("common", stEnStatPath, 118536)
SEADRAGON = Enemy("common", stEnStatPath, 120115)
DUCKSOLDIER = Enemy("common", stEnStatPath, 121694)
DUCKGENERAL = Enemy("common", stEnStatPath, 123273)
BARETTE = Enemy("common", stEnStatPath, 124852)
GOLDBARETTE = Enemy("common", stEnStatPath, 126431)
FIREDRAKE = Enemy("common", stEnStatPath, 128010)
BASILISK = Enemy("common", stEnStatPath, 129589)
WEREWOLF = Enemy("common", stEnStatPath, 131168)
BLACKFANG = Enemy("common", stEnStatPath, 132747)
SILVERWOLF = Enemy("common", stEnStatPath, 134326)
BLOODYWOLF = Enemy("common", stEnStatPath, 135905)
WOLFDEVIL = Enemy("common", stEnStatPath, 137484)
MEGACRAWLER = Enemy("common", stEnStatPath, 139063)
GIGACRAWLER = Enemy("common", stEnStatPath, 140642)
PETITDRAGON = Enemy("common", stEnStatPath, 142221)
FROSTDRAGON = Enemy("common", stEnStatPath, 143800)
PETITIAMATT = Enemy("common", stEnStatPath, 145379)
PETIDRAZOMBIE = Enemy("common", stEnStatPath, 146958)
CARMILLA = Enemy("common", stEnStatPath, 148537)
CARMILLAQUEEN = Enemy("common", stEnStatPath, 150116)
BOULDER = Enemy("common", stEnStatPath, 151695)
POWERBOULDER = Enemy("common", stEnStatPath, 153274)
LESSERDAEMON = Enemy("common", stEnStatPath, 154853)
GREATDAEMON = Enemy("common", stEnStatPath, 156432)
OGREBOX = Enemy("common", stEnStatPath, 158011)
KAISERMIMIC = Enemy("common", stEnStatPath, 159590)
Karl = Enemy("common", stEnStatPath, 162748)
Eagle = Enemy("common", stEnStatPath, 164327)
Bruiser = Enemy("common", stEnStatPath, 165906)
Bruiser2 = Enemy("common", stEnStatPath, 167485)


# ****** EnemyStatusStMaxStat - *****

stMaxStatPath = r'Game Files\uexp files\Orig\EnemyStatusMaxTable.uexp'

RABI = Enemy("common", stMaxStatPath, 111)
RABIRION = Enemy("common", stMaxStatPath, 1690)
KINGRABI = Enemy("common", stMaxStatPath, 3269)
GREATRABI = Enemy("common", stMaxStatPath, 4848)
MAIKONIDO = Enemy("common", stMaxStatPath, 6427)
DARTHMATANGO = Enemy("common", stMaxStatPath, 8006)
BATTOM = Enemy("common", stMaxStatPath, 9585)
DARKBATTOM = Enemy("common", stMaxStatPath, 11164)
GOBLIN = Enemy("common", stMaxStatPath, 12743)
GOBLINLORD = Enemy("common", stMaxStatPath, 14322)
BEASTMASTER = Enemy("common", stMaxStatPath, 15901)
BOUNDWOLF = Enemy("common", stMaxStatPath, 17480)
KERBEROS = Enemy("common", stMaxStatPath, 19059)
ASSASSINBUG = Enemy("common", stMaxStatPath, 20638)
RASTERBUG = Enemy("common", stMaxStatPath, 22217)
PORON = Enemy("common", stMaxStatPath, 23796)
POROBINHOOD = Enemy("common", stMaxStatPath, 25375)
POROBINLEADER = Enemy("common", stMaxStatPath, 26954)
ZOMBIE = Enemy("common", stMaxStatPath, 28533)
GHOUL = Enemy("common", stMaxStatPath, 30112)
SLIME = Enemy("common", stMaxStatPath, 31691)
SLIMEPRINCE = Enemy("common", stMaxStatPath, 33270)
MALLBEAR = Enemy("common", stMaxStatPath, 34849)
NIDORION = Enemy("common", stMaxStatPath, 36428)
GALBEE = Enemy("common", stMaxStatPath, 38007)
LADYBEE = Enemy("common", stMaxStatPath, 39586)
QUEENBEE = Enemy("common", stMaxStatPath, 41165)
UNICORNHEAD = Enemy("common", stMaxStatPath, 42744)
GOLDUNICO = Enemy("common", stMaxStatPath, 44323)
MAGICIAN = Enemy("common", stMaxStatPath, 45902)
WIZARD = Enemy("common", stMaxStatPath, 47481)
HIGHWIZARD = Enemy("common", stMaxStatPath, 49060)
MACHINEGOLEM = Enemy("common", stMaxStatPath, 50639)
GUARDIAN = Enemy("common", stMaxStatPath, 52218)
DEATHMACHINE = Enemy("common", stMaxStatPath, 53797)
COCKATRICE = Enemy("common", stMaxStatPath, 55376)
NEEDLEBIRD = Enemy("common", stMaxStatPath, 56955)
BIRD = Enemy("common", stMaxStatPath, 58534)
LITTLEDEVIL = Enemy("common", stMaxStatPath, 60113)
GREMLINS = Enemy("common", stMaxStatPath, 61692)
HARPY = Enemy("common", stMaxStatPath, 63271)
SEIREN = Enemy("common", stMaxStatPath, 64850)
ARMORNIGHT = Enemy("common", stMaxStatPath, 66429)
SILVERNIGHT = Enemy("common", stMaxStatPath, 68008)
SWORDNIGHT = Enemy("common", stMaxStatPath, 69587)
DARKLORD = Enemy("common", stMaxStatPath, 71166)
NINJA = Enemy("common", stMaxStatPath, 72745)
NINJAMASTER = Enemy("common", stMaxStatPath, 74324)
KNIGHTBLADE = Enemy("common", stMaxStatPath, 75903)
EVILSWORD = Enemy("common", stMaxStatPath, 77482)
ELEMENTSWORD = Enemy("common", stMaxStatPath, 79061)
SHAPESHIFTER = Enemy("common", stMaxStatPath, 80640)
SHADOWZERO = Enemy("common", stMaxStatPath, 82219)
SPECTRE = Enemy("common", stMaxStatPath, 93272)
GHOST = Enemy("common", stMaxStatPath, 94851)
DARKPRIEST = Enemy("common", stMaxStatPath, 96430)
EVILSHERMAN = Enemy("common", stMaxStatPath, 98009)
NECROMANCER = Enemy("common", stMaxStatPath, 99588)
GRELL = Enemy("common", stMaxStatPath, 101167)
GRELLMAGE = Enemy("common", stMaxStatPath, 102746)
PAKKUNOTAMA = Enemy("common", stMaxStatPath, 104325)
PAKKURIOTAMA = Enemy("common", stMaxStatPath, 105904)
PAKKUNTOKAGE = Enemy("common", stMaxStatPath, 107483)
PAKKUNDRAGON = Enemy("common", stMaxStatPath, 109062)
POT = Enemy("common", stMaxStatPath, 110641)
MAMAPOT = Enemy("common", stMaxStatPath, 112220)
PAPAPOT = Enemy("common", stMaxStatPath, 113799)
SAHUAGIN = Enemy("common", stMaxStatPath, 115378)
PETITPOSEIDON = Enemy("common", stMaxStatPath, 116957)
SEASERPENT = Enemy("common", stMaxStatPath, 118536)
SEADRAGON = Enemy("common", stMaxStatPath, 120115)
DUCKSOLDIER = Enemy("common", stMaxStatPath, 121694)
DUCKGENERAL = Enemy("common", stMaxStatPath, 123273)
BARETTE = Enemy("common", stMaxStatPath, 124852)
GOLDBARETTE = Enemy("common", stMaxStatPath, 126431)
FIREDRAKE = Enemy("common", stMaxStatPath, 128010)
BASILISK = Enemy("common", stMaxStatPath, 129589)
WEREWOLF = Enemy("common", stMaxStatPath, 131168)
BLACKFANG = Enemy("common", stMaxStatPath, 132747)
SILVERWOLF = Enemy("common", stMaxStatPath, 134326)
BLOODYWOLF = Enemy("common", stMaxStatPath, 135905)
WOLFDEVIL = Enemy("common", stMaxStatPath, 137484)
MEGACRAWLER = Enemy("common", stMaxStatPath, 139063)
GIGACRAWLER = Enemy("common", stMaxStatPath, 140642)
PETITDRAGON = Enemy("common", stMaxStatPath, 142221)
FROSTDRAGON = Enemy("common", stMaxStatPath, 143800)
PETITIAMATT = Enemy("common", stMaxStatPath, 145379)
PETIDRAZOMBIE = Enemy("common", stMaxStatPath, 146958)
CARMILLA = Enemy("common", stMaxStatPath, 148537)
CARMILLAQUEEN = Enemy("common", stMaxStatPath, 150116)
BOULDER = Enemy("common", stMaxStatPath, 151695)
POWERBOULDER = Enemy("common", stMaxStatPath, 153274)
LESSERDAEMON = Enemy("common", stMaxStatPath, 154853)
GREATDAEMON = Enemy("common", stMaxStatPath, 156432)
OGREBOX = Enemy("common", stMaxStatPath, 158011)
KAISERMIMIC = Enemy("common", stMaxStatPath, 159590)
Karl = Enemy("common", stMaxStatPath, 162748)
Eagle = Enemy("common", stMaxStatPath, 164327)
Bruiser = Enemy("common", stMaxStatPath, 165906)
Bruiser2 = Enemy("common", stMaxStatPath, 167485)
#endregion


#region Boss Instance Creation Start

# Charadata
# ****** EnemyStatusStbossSt - *****
stbossStPath = r'Game Files\Boss\Orig\uexp files\Charadata\BossStatusTable.uexp'
FullmetalHugger = Enemy("boss", stbossStPath, 140)
MachineGolemR = Enemy("boss", stbossStPath, 1764)
Jewel_EaterR = Enemy("boss", stbossStPath, 3388)
Zhenker = Enemy("boss", stbossStPath, 5012)
Genoa = Enemy("boss", stbossStPath, 6636)
Bill = Enemy("boss", stbossStPath, 8260)
Ben = Enemy("boss", stbossStPath, 9884)
Bill_and_Ben = Enemy("boss", stbossStPath, 11508)
Gorva = Enemy("boss", stbossStPath, 13132)
MachineGolemS = Enemy("boss", stbossStPath, 14756)
Beast_Ruger = Enemy("boss", stbossStPath, 16380)
Guilder_Vine = Enemy("boss", stbossStPath, 18004)
Land_amber = Enemy("boss", stbossStPath, 19628)
Feegu_Mund = Enemy("boss", stbossStPath, 21252)
Zan_Bie = Enemy("boss", stbossStPath, 22876)
Dangard = Enemy("boss", stbossStPath, 24500)
Mispolm = Enemy("boss", stbossStPath, 26124)
Doran = Enemy("boss", stbossStPath, 27748)
Light_Geizer = Enemy("boss", stbossStPath, 29372)
Sablehor = Enemy("boss", stbossStPath, 30996)
BlackKnight = Enemy("boss", stbossStPath, 32620)
CrimsonWizard = Enemy("boss", stbossStPath, 34244)
CrimsonWizardEvent = Enemy("boss", stbossStPath, 35868)
Man_eating_death = Enemy("boss", stbossStPath, 37492)
Fallen_saint = Enemy("boss", stbossStPath, 39116)
Earl_of_evil_eye = Enemy("boss", stbossStPath, 40740)
JewelryBeast = Enemy("boss", stbossStPath, 42364)
HugeDragon = Enemy("boss", stbossStPath, 43988)
DarkRich = Enemy("boss", stbossStPath, 45612)
ArchDemon = Enemy("boss", stbossStPath, 47236)
BlackRabi = Enemy("boss", stbossStPath, 48860)
MiniBlackRabi = Enemy("boss", stbossStPath, 50484)
Bruiser = Enemy("boss", stbossStPath, 52108)
Karl = Enemy("boss", stbossStPath, 53732)
Bill = Enemy("boss", stbossStPath, 55356)
Ben = Enemy("boss", stbossStPath, 56980)
Bill_and_Ben = Enemy("boss", stbossStPath, 58604)
Gorva = Enemy("boss", stbossStPath, 60228)
FullmetalHugger = Enemy("boss", stbossStPath, 61852)
Man_eating_death_Avatar = Enemy("boss", stbossStPath, 63476)
Jewel_Eater = Enemy("boss", stbossStPath, 65100)
Zhenker = Enemy("boss", stbossStPath, 66724)
Genoa = Enemy("boss", stbossStPath, 68348)
Guilder_Vine = Enemy("boss", stbossStPath, 69972)
Anise = Enemy("boss", stbossStPath, 71596)
AniseDragon = Enemy("boss", stbossStPath, 73220)
Sablehor_BlueMan = Enemy("boss", stbossStPath, 74844)
Sablehor_PurpleMan = Enemy("boss", stbossStPath, 76468)
ManaStone_Earth = Enemy("boss", stbossStPath, 78092)
ManaStone_Water = Enemy("boss", stbossStPath, 79716)
ManaStone_Fire = Enemy("boss", stbossStPath, 81340)
ManaStone_Wind = Enemy("boss", stbossStPath, 82964)
Anise_Avatar = Enemy("boss", stbossStPath, 84588)
ManaStone_Black = Enemy("boss", stbossStPath, 86212)
Mispolm_Ivy = Enemy("boss", stbossStPath, 87836)
Roki = Enemy("boss", stbossStPath, 89460)
BeastKing = Enemy("boss", stbossStPath, 91084)
Crystal = Enemy("boss", stbossStPath, 92708)
ArchDemon_ArmL = Enemy("boss", stbossStPath, 94332)
ArchDemon_ArmR = Enemy("boss", stbossStPath, 95956)
FullmetalHugger = Enemy("boss", stbossStPath, 97580)
Zhenker = Enemy("boss", stbossStPath, 99204)
Genoa = Enemy("boss", stbossStPath, 100828)
#endregion


#region Shinju Instance Creation Start

# ShinjuStatusTableList

# ****** EnemyStatusSteb11Custom0 - *****
steb11Custom0Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb11Custom\b11CustomStatusTable.uexp'
Land_amber = Enemy("shinju", steb11Custom0Path, 140)
Land_amber = Enemy("shinju", steb11Custom0Path, 1764)
Land_amber = Enemy("shinju", steb11Custom0Path, 3388)
Land_amber = Enemy("shinju", steb11Custom0Path, 5012)
Land_amber = Enemy("shinju", steb11Custom0Path, 6636)
Land_amber = Enemy("shinju", steb11Custom0Path, 8260)
Land_amber = Enemy("shinju", steb11Custom0Path, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb12_CustomStatusTable.uexp'
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 140)
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 1764)
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 3388)
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 5012)
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 6636)
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 8260)
Feegu_Mund = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb13_CustomStatusTable.uexp'
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 140)
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 1764)
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 3388)
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 5012)
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 6636)
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 8260)
Zan_Bie = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb14_CustomStatusTable.uexp'
Dangard = Enemy("shinju", stshinjuCustomPath, 140)
Dangard = Enemy("shinju", stshinjuCustomPath, 1764)
Dangard = Enemy("shinju", stshinjuCustomPath, 3388)
Dangard = Enemy("shinju", stshinjuCustomPath, 5012)
Dangard = Enemy("shinju", stshinjuCustomPath, 6636)
Dangard = Enemy("shinju", stshinjuCustomPath, 8260)
Dangard = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb15_02_CustomStatusTable.uexp'
Mispolm = Enemy("shinju", stshinjuCustomPath, 140)
Mispolm = Enemy("shinju", stshinjuCustomPath, 1764)
Mispolm = Enemy("shinju", stshinjuCustomPath, 3388)
Mispolm = Enemy("shinju", stshinjuCustomPath, 5012)
Mispolm = Enemy("shinju", stshinjuCustomPath, 6636)
Mispolm = Enemy("shinju", stshinjuCustomPath, 8260)
Mispolm = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb15_CustomStatusTable.uexp'
Mispolm = Enemy("shinju", stshinjuCustomPath, 140)
Mispolm = Enemy("shinju", stshinjuCustomPath, 1764)
Mispolm = Enemy("shinju", stshinjuCustomPath, 3388)
Mispolm = Enemy("shinju", stshinjuCustomPath, 5012)
Mispolm = Enemy("shinju", stshinjuCustomPath, 6636)
Mispolm = Enemy("shinju", stshinjuCustomPath, 8260)
Mispolm = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb16_CustomStatusTable.uexp'
Doran = Enemy("shinju", stshinjuCustomPath, 140)
Doran = Enemy("shinju", stshinjuCustomPath, 1764)
Doran = Enemy("shinju", stshinjuCustomPath, 3388)
Doran = Enemy("shinju", stshinjuCustomPath, 5012)
Doran = Enemy("shinju", stshinjuCustomPath, 6636)
Doran = Enemy("shinju", stshinjuCustomPath, 8260)
Doran = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusStshinjuCustom - *****
stshinjuCustomPath = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb17_CustomStatusTable.uexp'
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 140)
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 1764)
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 3388)
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 5012)
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 6636)
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 8260)
Light_Geizer = Enemy("shinju", stshinjuCustomPath, 9884)

# ****** EnemyStatusSteb_11Parts1 - *****
steb_11Parts1Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\01_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts1Path, 140)
ArmL = Enemy("shinju", steb_11Parts1Path, 1764)
ArmR = Enemy("shinju", steb_11Parts1Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts1Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts1Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts1Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts1Path, 9884)

# ****** EnemyStatusSteb_11Parts2 - *****
steb_11Parts2Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\02_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts2Path, 140)
ArmL = Enemy("shinju", steb_11Parts2Path, 1764)
ArmR = Enemy("shinju", steb_11Parts2Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts2Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts2Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts2Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts2Path, 9884)

# ****** EnemyStatusSteb_11Parts3 - *****
steb_11Parts3Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\03_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts3Path, 140)
ArmL = Enemy("shinju", steb_11Parts3Path, 1764)
ArmR = Enemy("shinju", steb_11Parts3Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts3Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts3Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts3Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts3Path, 9884)

# ****** EnemyStatusSteb_11Parts4 - *****
steb_11Parts4Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\04_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts4Path, 140)
ArmL = Enemy("shinju", steb_11Parts4Path, 1764)
ArmR = Enemy("shinju", steb_11Parts4Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts4Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts4Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts4Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts4Path, 9884)

# ****** EnemyStatusSteb_11Parts5 - *****
steb_11Parts5Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\05_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts5Path, 140)
ArmL = Enemy("shinju", steb_11Parts5Path, 1764)
ArmR = Enemy("shinju", steb_11Parts5Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts5Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts5Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts5Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts5Path, 9884)

# ****** EnemyStatusSteb_11Parts6 - *****
steb_11Parts6Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\06_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts6Path, 140)
ArmL = Enemy("shinju", steb_11Parts6Path, 1764)
ArmR = Enemy("shinju", steb_11Parts6Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts6Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts6Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts6Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts6Path, 9884)

# ****** EnemyStatusSteb_11Parts7 - *****
steb_11Parts7Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_11Parts\07_eb11_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_11Parts7Path, 140)
ArmL = Enemy("shinju", steb_11Parts7Path, 1764)
ArmR = Enemy("shinju", steb_11Parts7Path, 3388)
ArmL_Core01 = Enemy("shinju", steb_11Parts7Path, 5012)
ArmL_Core02 = Enemy("shinju", steb_11Parts7Path, 6636)
ArmR_Core01 = Enemy("shinju", steb_11Parts7Path, 8260)
ArmR_Core02 = Enemy("shinju", steb_11Parts7Path, 9884)

# ****** EnemyStatusSteb_12Parts8 - *****
steb_12Parts8Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\01_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts8Path, 140)
Body = Enemy("shinju", steb_12Parts8Path, 1764)
ArmL = Enemy("shinju", steb_12Parts8Path, 3388)
ArmR = Enemy("shinju", steb_12Parts8Path, 5012)
Tail = Enemy("shinju", steb_12Parts8Path, 6636)

# ****** EnemyStatusSteb_12Parts9 - *****
steb_12Parts9Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\02_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts9Path, 140)
Body = Enemy("shinju", steb_12Parts9Path, 1764)
ArmL = Enemy("shinju", steb_12Parts9Path, 3388)
ArmR = Enemy("shinju", steb_12Parts9Path, 5012)
Tail = Enemy("shinju", steb_12Parts9Path, 6636)

# ****** EnemyStatusSteb_12Parts10 - *****
steb_12Parts10Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\03_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts10Path, 140)
Body = Enemy("shinju", steb_12Parts10Path, 1764)
ArmL = Enemy("shinju", steb_12Parts10Path, 3388)
ArmR = Enemy("shinju", steb_12Parts10Path, 5012)
Tail = Enemy("shinju", steb_12Parts10Path, 6636)

# ****** EnemyStatusSteb_12Parts11 - *****
steb_12Parts11Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\04_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts11Path, 140)
Body = Enemy("shinju", steb_12Parts11Path, 1764)
ArmL = Enemy("shinju", steb_12Parts11Path, 3388)
ArmR = Enemy("shinju", steb_12Parts11Path, 5012)
Tail = Enemy("shinju", steb_12Parts11Path, 6636)

# ****** EnemyStatusSteb_12Parts12 - *****
steb_12Parts12Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\05_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts12Path, 140)
Body = Enemy("shinju", steb_12Parts12Path, 1764)
ArmL = Enemy("shinju", steb_12Parts12Path, 3388)
ArmR = Enemy("shinju", steb_12Parts12Path, 5012)
Tail = Enemy("shinju", steb_12Parts12Path, 6636)

# ****** EnemyStatusSteb_12Parts13 - *****
steb_12Parts13Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\06_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts13Path, 140)
Body = Enemy("shinju", steb_12Parts13Path, 1764)
ArmL = Enemy("shinju", steb_12Parts13Path, 3388)
ArmR = Enemy("shinju", steb_12Parts13Path, 5012)
Tail = Enemy("shinju", steb_12Parts13Path, 6636)

# ****** EnemyStatusSteb_12Parts14 - *****
steb_12Parts14Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_12Parts\07_eb12_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_12Parts14Path, 140)
Body = Enemy("shinju", steb_12Parts14Path, 1764)
ArmL = Enemy("shinju", steb_12Parts14Path, 3388)
ArmR = Enemy("shinju", steb_12Parts14Path, 5012)
Tail = Enemy("shinju", steb_12Parts14Path, 6636)

# ****** EnemyStatusSteb_13Parts15 - *****
steb_13Parts15Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\01_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts15Path, 140)
Altar_A = Enemy("shinju", steb_13Parts15Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts15Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts15Path, 5012)

# ****** EnemyStatusSteb_13Parts16 - *****
steb_13Parts16Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\02_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts16Path, 140)
Altar_A = Enemy("shinju", steb_13Parts16Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts16Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts16Path, 5012)

# ****** EnemyStatusSteb_13Parts17 - *****
steb_13Parts17Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\03_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts17Path, 140)
Altar_A = Enemy("shinju", steb_13Parts17Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts17Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts17Path, 5012)

# ****** EnemyStatusSteb_13Parts18 - *****
steb_13Parts18Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\04_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts18Path, 140)
Altar_A = Enemy("shinju", steb_13Parts18Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts18Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts18Path, 5012)

# ****** EnemyStatusSteb_13Parts19 - *****
steb_13Parts19Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\05_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts19Path, 140)
Altar_A = Enemy("shinju", steb_13Parts19Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts19Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts19Path, 5012)

# ****** EnemyStatusSteb_13Parts20 - *****
steb_13Parts20Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\06_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts20Path, 140)
Altar_A = Enemy("shinju", steb_13Parts20Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts20Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts20Path, 5012)

# ****** EnemyStatusSteb_13Parts21 - *****
steb_13Parts21Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_13Parts\07_eb13_01_PartsStatusTable.uexp'
Body = Enemy("shinju", steb_13Parts21Path, 140)
Altar_A = Enemy("shinju", steb_13Parts21Path, 1764)
Altar_B = Enemy("shinju", steb_13Parts21Path, 3388)
Altar_C = Enemy("shinju", steb_13Parts21Path, 5012)

# ****** EnemyStatusSteb_14Parts22 - *****
steb_14Parts22Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\01_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts22Path, 140)
Head02_R = Enemy("shinju", steb_14Parts22Path, 1764)

# ****** EnemyStatusSteb_14Parts23 - *****
steb_14Parts23Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\02_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts23Path, 140)
Head02_R = Enemy("shinju", steb_14Parts23Path, 1764)

# ****** EnemyStatusSteb_14Parts24 - *****
steb_14Parts24Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\03_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts24Path, 140)
Head02_R = Enemy("shinju", steb_14Parts24Path, 1764)

# ****** EnemyStatusSteb_14Parts25 - *****
steb_14Parts25Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\04_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts25Path, 140)
Head02_R = Enemy("shinju", steb_14Parts25Path, 1764)

# ****** EnemyStatusSteb_14Parts26 - *****
steb_14Parts26Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\05_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts26Path, 140)
Head02_R = Enemy("shinju", steb_14Parts26Path, 1764)

# ****** EnemyStatusSteb_14Parts27 - *****
steb_14Parts27Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\06_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts27Path, 140)
Head02_R = Enemy("shinju", steb_14Parts27Path, 1764)

# ****** EnemyStatusSteb_14Parts28 - *****
steb_14Parts28Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_14Parts\07_eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("shinju", steb_14Parts28Path, 140)
Head02_R = Enemy("shinju", steb_14Parts28Path, 1764)

# ****** EnemyStatusSteb_15Parts29 - *****
steb_15Parts29Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\01_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts29Path, 140)
Body = Enemy("shinju", steb_15Parts29Path, 1764)

# ****** EnemyStatusSteb_15Parts30 - *****
steb_15Parts30Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\02_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts30Path, 140)
Body = Enemy("shinju", steb_15Parts30Path, 1764)

# ****** EnemyStatusSteb_15Parts31 - *****
steb_15Parts31Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\03_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts31Path, 140)
Body = Enemy("shinju", steb_15Parts31Path, 1764)

# ****** EnemyStatusSteb_15Parts32 - *****
steb_15Parts32Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\04_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts32Path, 140)
Body = Enemy("shinju", steb_15Parts32Path, 1764)

# ****** EnemyStatusSteb_15Parts33 - *****
steb_15Parts33Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\05_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts33Path, 140)
Body = Enemy("shinju", steb_15Parts33Path, 1764)

# ****** EnemyStatusSteb_15Parts34 - *****
steb_15Parts34Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\06_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts34Path, 140)
Body = Enemy("shinju", steb_15Parts34Path, 1764)

# ****** EnemyStatusSteb_15Parts35 - *****
steb_15Parts35Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_15Parts\07_eb15_01_PartsStatusTable.uexp'
Head = Enemy("shinju", steb_15Parts35Path, 140)
Body = Enemy("shinju", steb_15Parts35Path, 1764)

# ****** EnemyStatusSteb_16Parts36 - *****
steb_16Parts36Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\01_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts36Path, 140)
Body = Enemy("shinju", steb_16Parts36Path, 1764)
HandLB = Enemy("shinju", steb_16Parts36Path, 3388)
HandRB = Enemy("shinju", steb_16Parts36Path, 5012)

# ****** EnemyStatusSteb_16Parts37 - *****
steb_16Parts37Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\02_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts37Path, 140)
Body = Enemy("shinju", steb_16Parts37Path, 1764)
HandLB = Enemy("shinju", steb_16Parts37Path, 3388)
HandRB = Enemy("shinju", steb_16Parts37Path, 5012)

# ****** EnemyStatusSteb_16Parts38 - *****
steb_16Parts38Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\03_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts38Path, 140)
Body = Enemy("shinju", steb_16Parts38Path, 1764)
HandLB = Enemy("shinju", steb_16Parts38Path, 3388)
HandRB = Enemy("shinju", steb_16Parts38Path, 5012)

# ****** EnemyStatusSteb_16Parts39 - *****
steb_16Parts39Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\04_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts39Path, 140)
Body = Enemy("shinju", steb_16Parts39Path, 1764)
HandLB = Enemy("shinju", steb_16Parts39Path, 3388)
HandRB = Enemy("shinju", steb_16Parts39Path, 5012)

# ****** EnemyStatusSteb_16Parts40 - *****
steb_16Parts40Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\05_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts40Path, 140)
Body = Enemy("shinju", steb_16Parts40Path, 1764)
HandLB = Enemy("shinju", steb_16Parts40Path, 3388)
HandRB = Enemy("shinju", steb_16Parts40Path, 5012)

# ****** EnemyStatusSteb_16Parts41 - *****
steb_16Parts41Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\06_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts41Path, 140)
Body = Enemy("shinju", steb_16Parts41Path, 1764)
HandLB = Enemy("shinju", steb_16Parts41Path, 3388)
HandRB = Enemy("shinju", steb_16Parts41Path, 5012)

# ****** EnemyStatusSteb_16Parts42 - *****
steb_16Parts42Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_16Parts\07_eb16_01_PartsTable.uexp'
Head = Enemy("shinju", steb_16Parts42Path, 140)
Body = Enemy("shinju", steb_16Parts42Path, 1764)
HandLB = Enemy("shinju", steb_16Parts42Path, 3388)
HandRB = Enemy("shinju", steb_16Parts42Path, 5012)

# ****** EnemyStatusSteb_17Parts43 - *****
steb_17Parts43Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\01_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts43Path, 140)
Body = Enemy("shinju", steb_17Parts43Path, 1764)

# ****** EnemyStatusSteb_17Parts44 - *****
steb_17Parts44Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\02_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts44Path, 140)
Body = Enemy("shinju", steb_17Parts44Path, 1764)

# ****** EnemyStatusSteb_17Parts45 - *****
steb_17Parts45Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\03_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts45Path, 140)
Body = Enemy("shinju", steb_17Parts45Path, 1764)

# ****** EnemyStatusSteb_17Parts46 - *****
steb_17Parts46Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\04_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts46Path, 140)
Body = Enemy("shinju", steb_17Parts46Path, 1764)

# ****** EnemyStatusSteb_17Parts47 - *****
steb_17Parts47Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\05_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts47Path, 140)
Body = Enemy("shinju", steb_17Parts47Path, 1764)

# ****** EnemyStatusSteb_17Parts48 - *****
steb_17Parts48Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\06_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts48Path, 140)
Body = Enemy("shinju", steb_17Parts48Path, 1764)

# ****** EnemyStatusSteb_17Parts49 - *****
steb_17Parts49Path = r'Game Files\Boss\Orig\uexp files\ShinjuStatusTableList\eb_17Parts\07_eb17_01_PartsStatusTable.uexp'
Eye = Enemy("shinju", steb_17Parts49Path, 140)
Body = Enemy("shinju", steb_17Parts49Path, 1764)
#endregion


#region Parts Instance Creation Start
# ****** eb01_01_PartsStatusTable - *****
eb01_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb01_01_PartsStatusTable.uexp'
Head = Enemy("parts", eb01_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb01_01_PartsStatusTable_Path, 1690)
ArmLB = Enemy("parts", eb01_01_PartsStatusTable_Path, 3269)
ArmRB = Enemy("parts", eb01_01_PartsStatusTable_Path, 4848)

# ****** eb01_02_PartsTable - *****
eb01_02_PartsTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb01_02_PartsTable.uexp'
Head = Enemy("parts", eb01_02_PartsTable_Path, 111)
Body = Enemy("parts", eb01_02_PartsTable_Path, 1690)
ArmLB = Enemy("parts", eb01_02_PartsTable_Path, 3269)
ArmRB = Enemy("parts", eb01_02_PartsTable_Path, 4848)

# ****** eb01_03_PartsTable - *****
eb01_03_PartsTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb01_03_PartsTable.uexp'
Head = Enemy("parts", eb01_03_PartsTable_Path, 111)
Body = Enemy("parts", eb01_03_PartsTable_Path, 1690)
ArmLB = Enemy("parts", eb01_03_PartsTable_Path, 3269)
ArmRB = Enemy("parts", eb01_03_PartsTable_Path, 4848)

# ****** eb03_01_PartsStatusTable - *****
eb03_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb03_01_PartsStatusTable.uexp'
None_part = Enemy("parts", eb03_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb03_01_PartsStatusTable_Path, 1690)
ArmL = Enemy("parts", eb03_01_PartsStatusTable_Path, 3269)
ArmR = Enemy("parts", eb03_01_PartsStatusTable_Path, 4848)
Tail = Enemy("parts", eb03_01_PartsStatusTable_Path, 6427)

# ****** eb03_11_PartsStatusTable - *****
eb03_11_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb03_11_PartsStatusTable.uexp'
None_part = Enemy("parts", eb03_11_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb03_11_PartsStatusTable_Path, 1690)
ArmL = Enemy("parts", eb03_11_PartsStatusTable_Path, 3269)
ArmR = Enemy("parts", eb03_11_PartsStatusTable_Path, 4848)
Tail = Enemy("parts", eb03_11_PartsStatusTable_Path, 6427)

# ****** eb07_01_PartsStatusTable - *****
eb07_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb07_01_PartsStatusTable.uexp'
Body = Enemy("parts", eb07_01_PartsStatusTable_Path, 111)
Shadow = Enemy("parts", eb07_01_PartsStatusTable_Path, 1690)
ShadowDummy1 = Enemy("parts", eb07_01_PartsStatusTable_Path, 3269)
ShadowDummy2 = Enemy("parts", eb07_01_PartsStatusTable_Path, 4848)
ShadowDummy3 = Enemy("parts", eb07_01_PartsStatusTable_Path, 6427)
ShadowDummy4 = Enemy("parts", eb07_01_PartsStatusTable_Path, 8006)
ShadowDummy5 = Enemy("parts", eb07_01_PartsStatusTable_Path, 9585)

# ****** eb07_11_PartsStatusTable - *****
eb07_11_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb07_11_PartsStatusTable.uexp'
Body = Enemy("parts", eb07_11_PartsStatusTable_Path, 111)
Shadow = Enemy("parts", eb07_11_PartsStatusTable_Path, 1690)
ShadowDummy1 = Enemy("parts", eb07_11_PartsStatusTable_Path, 3269)
ShadowDummy2 = Enemy("parts", eb07_11_PartsStatusTable_Path, 4848)
ShadowDummy3 = Enemy("parts", eb07_11_PartsStatusTable_Path, 6427)
ShadowDummy4 = Enemy("parts", eb07_11_PartsStatusTable_Path, 8006)
ShadowDummy5 = Enemy("parts", eb07_11_PartsStatusTable_Path, 9585)

# ****** eb10_01_PartsStatusTable - *****
eb10_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb10_01_PartsStatusTable.uexp'
Head = Enemy("parts", eb10_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb10_01_PartsStatusTable_Path, 1690)
ArmL = Enemy("parts", eb10_01_PartsStatusTable_Path, 3269)
ArmTipL = Enemy("parts", eb10_01_PartsStatusTable_Path, 4848)
ArmR = Enemy("parts", eb10_01_PartsStatusTable_Path, 6427)
ArmTipR = Enemy("parts", eb10_01_PartsStatusTable_Path, 8006)
Neck = Enemy("parts", eb10_01_PartsStatusTable_Path, 9585)
Flower = Enemy("parts", eb10_01_PartsStatusTable_Path, 11164)

# ****** eb10_11_PartsStatusTable - *****
eb10_11_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb10_11_PartsStatusTable.uexp'
Head = Enemy("parts", eb10_11_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb10_11_PartsStatusTable_Path, 1690)
ArmL = Enemy("parts", eb10_11_PartsStatusTable_Path, 3269)
ArmTipL = Enemy("parts", eb10_11_PartsStatusTable_Path, 4848)
ArmR = Enemy("parts", eb10_11_PartsStatusTable_Path, 6427)
ArmTipR = Enemy("parts", eb10_11_PartsStatusTable_Path, 8006)
Neck = Enemy("parts", eb10_11_PartsStatusTable_Path, 9585)
Flower = Enemy("parts", eb10_11_PartsStatusTable_Path, 11164)

# ****** eb11_01_PartsStatusTable - *****
eb11_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb11_01_PartsStatusTable.uexp'
Body = Enemy("parts", eb11_01_PartsStatusTable_Path, 111)
ArmL = Enemy("parts", eb11_01_PartsStatusTable_Path, 1690)
ArmR = Enemy("parts", eb11_01_PartsStatusTable_Path, 3269)
ArmL_Core01 = Enemy("parts", eb11_01_PartsStatusTable_Path, 4848)
ArmL_Core02 = Enemy("parts", eb11_01_PartsStatusTable_Path, 6427)
ArmR_Core01 = Enemy("parts", eb11_01_PartsStatusTable_Path, 8006)
ArmR_Core02 = Enemy("parts", eb11_01_PartsStatusTable_Path, 9585)

# ****** eb12_01_PartsStatusTable - *****
eb12_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb12_01_PartsStatusTable.uexp'
Head = Enemy("parts", eb12_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb12_01_PartsStatusTable_Path, 1690)
ArmL = Enemy("parts", eb12_01_PartsStatusTable_Path, 3269)
ArmR = Enemy("parts", eb12_01_PartsStatusTable_Path, 4848)
Tail = Enemy("parts", eb12_01_PartsStatusTable_Path, 6427)

# ****** eb13_01_PartsStatusTable - *****
eb13_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb13_01_PartsStatusTable.uexp'
Body = Enemy("parts", eb13_01_PartsStatusTable_Path, 111)
Altar_A = Enemy("parts", eb13_01_PartsStatusTable_Path, 1690)
Altar_B = Enemy("parts", eb13_01_PartsStatusTable_Path, 3269)
Altar_C = Enemy("parts", eb13_01_PartsStatusTable_Path, 4848)

# ****** eb14_01_PartsStatusTable - *****
eb14_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb14_01_PartsStatusTable.uexp'
Head01_L = Enemy("parts", eb14_01_PartsStatusTable_Path, 111)
Head02_R = Enemy("parts", eb14_01_PartsStatusTable_Path, 1690)

# ****** eb15_01_PartsTable - *****
eb15_01_PartsTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb15_01_PartsTable.uexp'
Head = Enemy("parts", eb15_01_PartsTable_Path, 111)
Body = Enemy("parts", eb15_01_PartsTable_Path, 1690)

# ****** eb15_02_PartsTable - *****
eb15_02_PartsTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb15_02_PartsTable.uexp'
Head = Enemy("parts", eb15_02_PartsTable_Path, 111)

# ****** eb16_01_PartsTable - *****
eb16_01_PartsTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb16_01_PartsTable.uexp'
Head = Enemy("parts", eb16_01_PartsTable_Path, 111)
Body = Enemy("parts", eb16_01_PartsTable_Path, 1690)
HandLB = Enemy("parts", eb16_01_PartsTable_Path, 3269)
HandRB = Enemy("parts", eb16_01_PartsTable_Path, 4848)

# ****** eb17_01_PartsStatusTable - *****
eb17_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb17_01_PartsStatusTable.uexp'
Eye = Enemy("parts", eb17_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb17_01_PartsStatusTable_Path, 1690)

# ****** eb21_01_PartsStatusTable - *****
eb21_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb21_01_PartsStatusTable.uexp'
Body = Enemy("parts", eb21_01_PartsStatusTable_Path, 111)
RouletteDeath_Actor01 = Enemy("parts", eb21_01_PartsStatusTable_Path, 1690)
RouletteDeath_Actor02 = Enemy("parts", eb21_01_PartsStatusTable_Path, 3269)
RouletteDeath_Actor03 = Enemy("parts", eb21_01_PartsStatusTable_Path, 4848)
RouletteDeath_Actor04 = Enemy("parts", eb21_01_PartsStatusTable_Path, 6427)

# ****** eb25_01_PartsStatusTable - *****
eb25_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb25_01_PartsStatusTable.uexp'
None_part = Enemy("parts", eb25_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb25_01_PartsStatusTable_Path, 1690)
ArmL = Enemy("parts", eb25_01_PartsStatusTable_Path, 3269)
ArmR = Enemy("parts", eb25_01_PartsStatusTable_Path, 4848)
Tail = Enemy("parts", eb25_01_PartsStatusTable_Path, 6427)
None_part = Enemy("parts", eb25_01_PartsStatusTable_Path, 8006)
None_part = Enemy("parts", eb25_01_PartsStatusTable_Path, 9585)
None_part = Enemy("parts", eb25_01_PartsStatusTable_Path, 11164)

# ****** eb27_01_PartsStatusTable - *****
eb27_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb27_01_PartsStatusTable.uexp'
Body = Enemy("parts", eb27_01_PartsStatusTable_Path, 111)
ArmL = Enemy("parts", eb27_01_PartsStatusTable_Path, 1690)
ArmR = Enemy("parts", eb27_01_PartsStatusTable_Path, 3269)
SpiralMoon_Gimmick01 = Enemy("parts", eb27_01_PartsStatusTable_Path, 4848)
HellSouthernCross_Gimick01 = Enemy("parts", eb27_01_PartsStatusTable_Path, 6427)
HellSouthernCross_Gimick02 = Enemy("parts", eb27_01_PartsStatusTable_Path, 8006)
Gigaburn_Gimmick01 = Enemy("parts", eb27_01_PartsStatusTable_Path, 9585)
Gigaburn_Gimmick02 = Enemy("parts", eb27_01_PartsStatusTable_Path, 11164)
Gigaburn_Gimmick03 = Enemy("parts", eb27_01_PartsStatusTable_Path, 12743)

# ****** eb33_01_PartsStatusTable - *****
eb33_01_PartsStatusTable_Path = r'Game Files\Boss\Orig\uexp files\Parts\eb33_01_PartsStatusTable.uexp'
Head = Enemy("parts", eb33_01_PartsStatusTable_Path, 111)
Body = Enemy("parts", eb33_01_PartsStatusTable_Path, 1690)
#endregion


with open('multipliers-config.yaml', 'r') as file:
    multipliersDict = yaml.load(file, Loader=yaml.FullLoader)

makeDirectories()

for enemyType in ['common', 'boss', 'shinju', 'parts']:
    editHexAll(enemyType)  


print("Please check that the directory 'Custom_TofMania - 0.3.2_P' has new files created.\n" \
        "If the files existed before running this script, they should be updated now.\n")

closeVar = input("Press 'enter' to exit the console.")
closeVar = None
