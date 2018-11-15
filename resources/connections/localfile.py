import os, re
from resources.common.fileops import checkPath, copyFile, deleteFile, osPathFromString
from resources.common.remotesites import parseSettings

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        self.REMOTEPATH = osPathFromString( settings.get( 'path' ) )
        self.DELETEAFTERDOWNLOAD = settings.get( 'deleteafterdownload' )
    
    
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
            if re.search( self.REMOTEFILTER, file ):
                srcpath = os.path.join( self.REMOTEPATH, file )
                dstpath = os.path.join( self.LOCALDOWNLOADPATH, file )
                success, cloglines = copyFile( src=srcpath, dst=dstpath )
                loglines.extend( cloglines )
                if success:
                    dlist.append( file )
                    if self.DELETEAFTERDOWNLOAD:
                        success, dloglines = deleteFile( srcpath )
                        loglines.extend( dloglines )
        return dlist, loglines
        

    def Upload( self, files ):
        if not self.REMOTEPATH:
            return False, ['no remote directory path defined, aborting']
        loglines = []
        overall_success = True
        for file in files:
            srcpath = os.path.join( self.LOCALDOWNLOADPATH, file )
            remotefolder = os.path.join( self.REMOTEPATH, self.SOURCEFOLDER )
            success, cloglines = checkPath( remotefolder )
            if not success:
                loglines.extend( cloglines )
            destpath = os.path.join( remotefolder, file )
            success, cloglines = copyFile( src=srcpath, dst=destpath )
            loglines.extend( cloglines )
            if not success:
                overall_sucess = False
        if not overall_success:
            loglines.append( ['one or more files was not copied'] )
        return overall_success, loglines
