import chilkat, datetime, os
from ..common.hostkeys import CheckHostKey

class Source:
    def __init__( self, dataroot, config, override_date ):
        self.DATAROOT = dataroot
        self.CHILKATLICENSE = config.Get( 'chilkat_license' )
        self.HOSTKEY = os.path.join( dataroot, 'commonapp_hostkey' )
        self.HOST = config.Get( 'commonapp_baseURL' )
        self.USERNAME = config.Get( 'commonapp_user' )
        self.AUTH = config.Get( 'commonapp_auth' )
        self.PORT = config.Get( 'commonapp_port' )
        self.TIMEOUT = config.Get( 'commonapp_timeout' )
        self.PATH = config.Get( 'commonapp_path' )
        key = chilkat.CkSshKey()
        key_auth = config.Get( 'commonapp_key_auth' )
        privatekey = key.loadText( os.path.join( dataroot, config.Get( 'commonapp_key' ) ) )
        if key.get_LastMethodSuccess() == True:
            if key_auth:
                key.put_Password( key_auth );
            success = key.FromOpenSshPrivateKey( privatekey )
            if (success == True):
                self.KEY = key
            else:
                self.KEY = None   
        else:
            self.KEY = None
        if override_date:
            self.STRTODAY = override_date
        else:
            self.STRTODAY = datetime.date.today().strftime( config.Get( 'commonapp_dateformat' ) )
        self.DEBUG = config.Get( 'debug' )
    
    
    def Retrieve( self ):
        loglines = []
        dlist = []
        loglines.append( 'connecting to Common App server' )
        sftp = chilkat.CkSFtp()
        success = sftp.UnlockComponent( self.CHILKATLICENSE )
        if (success != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        sftp.put_ConnectTimeoutMs( self.TIMEOUT )
        sftp.put_IdleTimeoutMs( self.TIMEOUT )
        success = sftp.Connect( self.HOST, self.PORT )
        if (success != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        success, cloglines = CheckHostKey( sftp.hostKeyFingerprint(), self.HOSTKEY )
        if self.DEBUG:
            loglines.extend( cloglines )
        if not success:
            loglines.append( 'WARNING: HOSTKEY FOR COMMONAPP SERVER DOES NOT MATCH SAVED KEY. ABORTING.' )
            return False, loglines
        if self.KEY:
            loglines.append( 'trying to authentication using private key' )
            success = sftp.AuthenticatePk( self.USERNAME, self.KEY )
        else:
            success = False
        if (success != True):
            if self.KEY and self.DEBUG:
                loglines.append( sftp.lastErrorText() )
            elif self.KEY:
                loglines.append( 'private key based authentication failed' )
            loglines.append( 'trying to authentication with username and password' )
            success = sftp.AuthenticatePw( self.USERNAME, self.AUTH )
            if (success != True):
                loglines.append( sftp.lastErrorText() )
                return False, loglines
        success = sftp.InitializeSftp()
        if (success != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        handle = sftp.openDir( self.PATH )
        if (sftp.get_LastMethodSuccess() != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        dirlisting = sftp.ReadDir( handle )
        if (sftp.get_LastMethodSuccess() != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
        if self.PATH == '.':
            remotepath = ''
        n = dirlisting.get_NumFilesAndDirs()
        if n == 0:
            loglines.append( 'no files in Common App directory' )
        else:
            for i in range( 0, n ):
                filename = dirlisting.GetFileObject( i ).filename()
                remotefile = remotepath + filename
                if self.DEBUG:
                    loglines.append( 'checking file ' + filename )
                if self.STRTODAY in filename:
                    localfile = os.path.join( self.DATAROOT, filename )
                    success = sftp.DownloadFileByName( remotefile, localfile )
                    if success == True:
                        loglines.append( 'downloaded %s to %s' % (remotefile, localfile) )
                        dlist.append( filename )
                    else:
                        loglines.append( 'unable to download %s to %s' % (remotefile, localfile) )
                        if self.DEBUG:
                           loglines.append( sftp.lastErrorText() ) 
        success = sftp.CloseHandle( handle )
        if (success != True) and self.DEBUG:
            loglines.append( sftp.lastErrorText() )
        if not dlist:
            loglines.append( 'no Common App files for today' )
        return dlist, loglines