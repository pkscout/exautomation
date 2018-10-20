import os
from datetime import datetime, date, timedelta
from ..common.fileops import copyFile

class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
        self.CONFIG = {}
        self.CONFIG['debug'] = config.Get( 'debug' )     
        self.REMOTEPATH = settings.get( 'path' )
        if settings.get( 'override_date' ) and settings.get( 'override_date' ) != 'all':
            try:
                filedate = datetime.strptime( settings.get( 'override_date' ), config.Get( 'override_dateformat' ) ).date()
            except ValueError as e:
                print( 'Error: ' + str( e ) )
                raise ValueError( str( e ) )
        else:
            filedate = date.today() - timedelta(1)
        self.FILEDATE = filedate.strftime( settings.get( 'dateformat', config.Get( 'dateformat' ) ) )
    
    
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
            if self.FILEDATE in file:
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
        
        
