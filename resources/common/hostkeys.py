# v.0.1.0

from .fileops import readFile, writeFile

def CheckHostKey( key, file ):
    loglines = []
    rloglines, saved_key = readFile( file )
    loglines.extend( rloglines )
    if not saved_key:
        success, wloglines = writeFile( key, file, 'w' )
        loglines.extend( wloglines )
        saved_key = key
    return saved_key == key, loglines
