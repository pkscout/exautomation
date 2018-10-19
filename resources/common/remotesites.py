# v.0.1.0
    
import chilkat, os
from .fileops import readFile, writeFile
from .hostkeys import CheckHostKey
    
class SFTP:
    def __init__( self, config ):
        self.CONFIG = config
    
    
    def _connect( self ):
        loglines = []
        key = chilkat.CkSshKey()
        privatekey = key.loadText( self.CONFIG.get( 'privatekeypath' ) )
        if key.get_LastMethodSuccess() == True:
            if self.CONFIG.get( 'key_auth' ):
                key.put_Password( self.CONFIG.get( 'key_auth' ) );
            success = key.FromOpenSshPrivateKey( privatekey )
            if not success:
                key = None   
        else:
            key = None
        loglines.append( 'connecting to %s server' % self.CONFIG.get( 'module_name', '' ) )
        sftp = chilkat.CkSFtp()
        success = sftp.UnlockComponent( self.CONFIG.get( 'chilkat_license', 'Anything for 30 day trial' ) )
        if not success:
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        sftp.put_ConnectTimeoutMs( self.CONFIG.get( 'timeout', 15000 ) )
        sftp.put_IdleTimeoutMs( self.CONFIG.get( 'timeout', 15000 ) )
        success = sftp.Connect( self.CONFIG.get( 'host' ), self.CONFIG.get( 'port', 22 ) )
        if not success:
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        success, cloglines = CheckHostKey( sftp.hostKeyFingerprint(), self.CONFIG.get( 'hostkey' ) )
        if self.CONFIG.get( 'debug' ):
            loglines.extend( cloglines )
        if not success:
            loglines.append( 'WARNING: HOSTKEY FOR %s SERVER DOES NOT MATCH SAVED KEY. ABORTING.' % self.CONFIG.get( 'module_name', '' ).upper() )
            return False, loglines
        if key:
            loglines.append( 'trying to authentication using private key' )
            success = sftp.AuthenticatePk( self.CONFIG.get( 'username', '' ), key )
        else:
            success = False
        if not success:
            if key and self.CONFIG.get( 'debug' ):
                loglines.append( sftp.lastErrorText() )
            elif key:
                loglines.append( 'private key based authentication failed' )
            loglines.append( 'trying to authentication with username and password' )
            success = sftp.AuthenticatePw( self.CONFIG.get( 'username', '' ), self.CONFIG.get( 'auth', '' ) )
            if not success:
                loglines.append( sftp.lastErrorText() )
                return False, loglines
        success = sftp.InitializeSftp()
        if not success:
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        return sftp, loglines
 
 
    def Download( self, destination, filter='', path='.' ):
        loglines = []
        dlist = []
        sftp, cloglines = self._connect()
        loglines.extend( cloglines )
        if not sftp:
            return False, loglines
        handle = sftp.openDir( path )
        if (sftp.get_LastMethodSuccess() != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        dirlisting = sftp.ReadDir( handle )
        if (sftp.get_LastMethodSuccess() != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        if path == '.':
            remotepath = ''
        n = dirlisting.get_NumFilesAndDirs()
        if n == 0:
            loglines.append( 'no files in directory' )
        else:
            for i in range( 0, n ):
                filename = dirlisting.GetFileObject( i ).filename()
                remotefile = remotepath + filename
                if self.CONFIG.get( 'debug' ):
                    loglines.append( 'checking file ' + filename )
                if filter in filename:
                    localfile = os.path.join( destination, filename )
                    success = sftp.DownloadFileByName( remotefile, localfile )
                    if success == True:
                        loglines.append( 'downloaded %s to %s' % (remotefile, localfile) )
                        dlist.append( filename )
                    else:
                        loglines.append( 'unable to download %s to %s' % (remotefile, localfile) )
                        if self.CONFIG.get( 'debug' ):
                           loglines.append( sftp.lastErrorText() ) 
        success = sftp.CloseHandle( handle )
        if not success and self.CONFIG.get( 'debug' ):
            loglines.append( sftp.lastErrorText() )
        if not dlist:
            loglines.append( ['no files matching filter ' + filter] )
        return dlist, loglines
   


class FTPS:    
    def __init__( self, config ):
        self.CONFIG = config

    
    def _connect( self ):
        loglines = []
        ftps = chilkat.CkFtp2()
        success = ftps.UnlockComponent( self.CONFIG.get( 'chilkat_license', 'Anything for 30 day trial' ) )
        if not success:
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        loglines.append( 'connecting to %s server' % self.CONFIG.get( 'module_name', '' ) )
        ftps.put_Passive( self.CONFIG.get( 'passive', False ) )
        ftps.put_Hostname( self.CONFIG.get( 'host' ) )
        ftps.put_Username( self.CONFIG.get( 'username' ) )
        ftps.put_Password( self.CONFIG.get( 'auth' ) )
        ftps.put_Port( self.CONFIG.get( 'port', 990 ) )
        ftps.put_AuthTls( self.CONFIG.get( 'authtls', True ) )
        ftps.put_Ssl( self.CONFIG.get( 'ssl', False ) )
        success = ftps.Connect()
        if not success:
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        return ftps, loglines
    

    def Download( self, destination, filter='', path='' ):
        loglines = []
        dlist = []
        ftps, cloglines = self._connect()
        loglines.extend( cloglines )
        if not ftps:
            return False, loglines
        if path:
            success = ftps.ChangeRemoteDir( path )
            if not success:
                loglines.append( ftps.lastErrorText() )
                return False, loglines
        n = ftps.GetDirCount()
        if n < 0:
            loglines.append( ftps.lastErrorText() )
            return False, loglines        
        elif n == 0:
            loglines.append( 'no files in directory' )
        else:
            for i in range( 0, n ):
                filename = ftps.getFilename( i )
                if self.CONFIG.get( 'debug' ):
                    loglines.append( 'checking file ' + filename )
                if filter in filename:
                    localfile = os.path.join( destination, filename )
                    success = ftps.GetFile( filename, localfile )
                    if success == True:
                        loglines.append( 'downloaded %s to %s' % (filename, localfile) )
                        dlist.append( filename )
                    else:
                        loglines.append( 'unable to download %s to %s' % (filename, localfile) )
                        if self.CONFIG.get( 'debug' ):
                           loglines.append( sftp.lastErrorText() ) 

        success = ftps.Disconnect()
        if not success and self.CONFIG.get( 'debug' ):
            loglines.append( sftp.lastErrorText() )
        return dlist, loglines


    def Upload( self, files, origin, path='' ):
        loglines = []
        ftps, cloglines = self._connect()
        loglines.extend( cloglines )
        if not ftps:
            return False, loglines
        success = ftps.ChangeRemoteDir( path )
        if not success:
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        loglines.append( 'setting destination directory to ' + path )
        loglines.append( 'transferring files to FTPS server' )
        fsuccess = True
        for file in files:        
            loglines.append( 'transferring file ' + file )
            filepath = os.path.join( origin, file )
            success = ftps.PutFile( filepath, file )
            if not success:
                loglines.append( ftps.lastErrorText() )
                fsuccess = False
        loglines.append( 'disconnecting from FTPS server' )
        success = ftps.Disconnect()
        if not success and self.CONFIG.get( 'debug' ):
            loglines.append( sftp.lastErrorText() )
        return fsuccess, loglines

    