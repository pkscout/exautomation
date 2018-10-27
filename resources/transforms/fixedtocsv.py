import csv, os, pathlib
from ..common.fileops import readFile

class Transform:
    def Run( self, orgfile, destfile, settings, debug ):
        loglines = []
        encoding = settings.get( 'encoding' )
        colspec = settings.get( 'colspec' )
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
        if not destfile.endswith('.csv'):
            destpath = pathlib.PurePath( destfile )
            destfile = os.path.join( destpath.parent, destpath.stem + '.csv' )
        with open( destfile, "w" ) as result:
            if settings.get( 'quoteall', True ):
                wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
            else:
                wtr = csv.writer( result )
            if settings.get( 'header' ):
                wtr.writerow( settings.get( 'header' ) )
            for row in data:
                wtr.writerow( row )
        return destfile, loglines

