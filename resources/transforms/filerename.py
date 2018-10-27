import os, re, pathlib
from datetime import date
from ..common.fileops import copyFile

class Transform:
    def Run( self, orgfile, destfile, settings, debug ):
        loglines = []
        if not settings.get( 'search' ) or not settings.get( 'replace' ):
            return False, ['search or replace settings not included, aborting transform.']
        destpath = pathlib.PurePath( destfile )
        newname = re.sub( settings.get( 'search' ), settings.get( 'replace' ), destpath.name )            
        destfile = os.path.join( destpath.parent, newname )
        if settings.get( 'appendstring' ):
            datestring = settings.get( 'string', (date.today().strftime( settings.get( 'dateformat', '%Y-%m-%d' ) ) ) )
            destpath = pathlib.PurePath( destfile )
            destfile = os.path.join( destpath.parent, destpath.stem + '-' + datestring + destpath.suffix )
        success, cloglines = copyFile( orgfile, destfile )
        if settings.get( 'debug' ):
            loglines.extended( cloglines )
        if not success:
            return False, loglines
        return destfile, loglines

