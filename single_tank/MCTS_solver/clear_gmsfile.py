import os
import numpy as np

formatFiles = [
    '.py',
    '.pyc',
    '.csv'
]

keepFileName = [
    'singletankNz1',
    'singletankNz2',
    'singletankNz3',
    'singletankNz4',
    'singletankNz5',
    'singletankNz8',
    'singletankNz10',
    'sigletankdataNz1n',
    'sigletankdataNz1p',
    'sigletankdataNz2n',
    'sigletankdataNz2p',
    'sigletankdataNz3n',
    'sigletankdataNz3p',
    'sigletankdataNz4n',
    'sigletankdataNz4p',
    'sigletankdataNz5n',
    'sigletankdataNz5p',
    'sigletankdataNz8n',
    'sigletankdataNz8p',
    'sigletankdataNz10n',
    'sigletankdataNz10p'
]

def delFile(filePath):
    formatName = os.path.splitext(filePath)[1]
    if not formatFiles.__contains__(formatName) and filePath.split('/')[-1] != '.DS_Store':
        fpathandname, fext = os.path.splitext(filePath)
        #print(fpathandname)
        fname = fpathandname.split('\\')[-1]
        if keepFileName.__contains__(fname) :
            print(fname)
            #print("GAMS source file shouldnot delete.")
        else :
            #print(fext)
            os.remove(filePath)
    


def currentDirFile(deldir):
    fileNames = os.listdir(deldir)
    for fn in fileNames:
        fullFileName = os.path.join(deldir, fn)
        if not os.path.isdir(fullFileName):
            delFile(fullFileName)
        else:
            currentDirFile(fullFileName)

def clearfile():
    deldir = os.getcwd()
    print("search dir:",deldir)
    currentDirFile(deldir)

if __name__ == "__main__": 
    deldir = os.getcwd()
    print("search dir:",deldir)
    currentDirFile(deldir)