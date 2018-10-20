import os, re
from datetime import datetime, date, timedelta
from ..common.fileops import copyFile

class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
        if settings.get( 'override_date' ):
            dateformat = config.Get( 'override_dateformat' )
        else:
            dateformat = settings.get( 'dateformat', config.Get( 'override_dateformat' ) )
        thedate = settings.get( 'override_date', settings.get( 'filter' ) )
        try:
            self.FILTER = datetime.strptime( thedate, dateformat ).date()
        except TypeError as e:
            self.FILTER = (date.today() - timedelta( 1 )).strftime( dateformat )
        except ValueError as e:        
            self.FILTER = thedate
        self.REMOTEPATH = settings.get( 'path' )
    
    
    def Download( self ):
        if not self.REMOTEPATH:
            return False, ['no remote directory path defined, aborting']
        loglines = []
        dlist = []
        try:
            dirlist = os.listdir( self.REMOTEPATH )
        except OSError as e:
            return False, ['unable to get directory listing for ' + self.REMOTEPATH, str( e )]
        for file in dirlist:
            if re.search( self.FILTER, file ):
                srcpath = os.path.join( self.REMOTEPATH, file )
                dstpath = os.path.join( self.DATAROOT, 'downloads', file )
                success, cloglines = copyFile( src=srcpath, dst=dstpath )
                loglines.extend( cloglines )
                if success:
                    dlist.append( file )
        return dlist, loglines
        

    def Upload( self, files ):
        if not self.REMOTEPATH:
            return False, ['no remote directory path defined, aborting']
        loglines = []
        overall_success = True
        for file in files:
            srcpath = os.path.join( self.DATAROOT, 'downloads', file )
            destpath = os.path.join( self.REMOTEPATH, file )
            success, cloglines = copyFile( src=srcpath, dst=destpath )
            loglines.extend( cloglines )
            if not success:
                overall_sucess = False
        if not overall_success:
            loglines.append( ['one or more files was not copied'] )
        return overall_success, loglines
        
        
