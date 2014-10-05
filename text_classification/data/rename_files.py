import os, sys
import codecs
dataFolder = 'data'
folder = os.path.dirname(os.path.abspath(__file__))+'\\'
folder =  folder + '\\corpora\\raw\\en\\bitcoin\\twitter\\'
#folder = sharedFolderPath

for dirname, dirnames, filenames in os.walk(folder):
    for subdirname in dirnames:
        #className = subdirname
        print("subdirname", subdirname)
    for filename in filenames:
        if len(filename.split("__"))>1:
            fullpath = os.path.join(dirname, filename)
            fileExtension = os.path.splitext(filename)[1]
            print("dirname: ", dirname, ", filename: ", filename, ", fullpath: ", fullpath)
            print("change to")
            new_filename = filename.split("__")[0] + fileExtension
            new_fullpath = os.path.join(dirname, new_filename)
            print(new_fullpath)
            print(os.rename(fullpath,new_fullpath))