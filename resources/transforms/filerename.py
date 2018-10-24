import os, re, pathlib
from ..common.fileops import copyFile

class Transform:
    def Run( self, orgfile, destfile, settings ):
        loglines = []
        if not settings.get( 'search' ) and settings.get( 'replace' ):
            return False, ['search or replace settings not included, aborting transform.']
        destpath = pathlib.PurePath( destfile )
        newname = re.sub( settings.get( 'search' ), settings.get( 'replace' ), destpath.name )
        destfile = os.path.join( destpath.parent, newname )
        success, cloglines = copyFile( orgfile, destfile )
        if settings.get( 'debug' ):
            loglines.extended( cloglines )
        if not success:
            return False, loglines
        return destfile, loglines

