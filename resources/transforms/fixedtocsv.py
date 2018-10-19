import csv
from ..common.fileops import readFile

class Transform:
    def __init__( self ):
        pass


    def Run( self, orgfile, destfile, config ):
        loglines = []
        encoding = config.get( 'encoding', 'utf-8-sig' )
        colspec = config.get( 'colspec' )
        if not colspec:
            return False, ['no column specifications provided, aborting']
        if encoding:
            f = open( orgfile, mode='r', encoding=encoding )
        else:
            f = open( orgfile, mode='r' )
        lines = f.readlines()
        f.close()
        data = []
        for line in lines:
            entry = []
            for col in colspec:
                item = line[col[0]-1:col[1]].strip()
                entry.append( item )
            data.append( entry )
        with open( destfile, "w" ) as result:
            if config.get( 'quoteall', True ):
                wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
            else:
                wtr = csv.writer( result )
            if config.get( 'header' ):
                wtr.writerow( config.get( 'header' ) )
            for row in data:
                wtr.writerow( row )
        return True, loglines

