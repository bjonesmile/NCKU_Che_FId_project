import os
import numpy as np

formatFiles = [
    '.py',
    '.pyc'
]

keepFileName = [
    'tank1sol',
    'alcoholicCSTRNz1',
    'alcoholicCSTRNz2',
    'alcoholicCSTRNz3',
    'alcoholicCSTRNz4',
    'alcoholicCSTRNz5',
    'alcoholicCSTRNz6',
    'alcoholicCSTRNz8',
    'alcoholicCSTRNz10',
    'alcoholicCSTRNz12',
    'alcoholicCSTRNz15',
    'alcoholicCSTRNz20',
    'alcoholicCSTRNz1n',
    'alcoholicCSTRNz1p',
    'alcoholicCSTRNz2n',
    'alcoholicCSTRNz2p',
    'alcoholicCSTRNz3n',
    'alcoholicCSTRNz3p',
    'alcoholicCSTRNz4n',
    'alcoholicCSTRNz4p',
    'alcoholicCSTRNz5n',
    'alcoholicCSTRNz5p',
    'alcoholicCSTRNz6n',
    'alcoholicCSTRNz6p',
    'alcoholicCSTRNz8n',
    'alcoholicCSTRNz8p',
    'alcoholicCSTRNz10n',
    'alcoholicCSTRNz10p',
    'alcoholicCSTRNz12n',
    'alcoholicCSTRNz12p',
    'alcoholicCSTRNz15n',
    'alcoholicCSTRNz15p',
    'alcoholicCSTRNz20n',
    'alcoholicCSTRNz20p'
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