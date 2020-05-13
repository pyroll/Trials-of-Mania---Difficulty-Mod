import os


eneDataDir = 'parsed_ene_data'    

for root, dirs, files in os.walk(eneDataDir):
    for file in files:
        # This will concatenate the 'head' and 'tail' to form the full file path
        fullPath = os.path.join(root, file)
        print(fullPath)