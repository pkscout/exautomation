import datetime, os
from ..common.remotesites import ConnectSFTP

class Source:
    def __init__( self, dataroot, config, override_date ):
        self.DATAROOT = dataroot
        self.CONFIG = {}
        self.CONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONFIG['module_name'] = 'Common App'
        self.CONFIG['hostkey'] = os.path.join( dataroot, 'commonapp_hostkey' )
        self.CONFIG['host'] = config.Get( 'commonapp_baseURL' )
        self.CONFIG['privatekeypath'] = os.path.join( dataroot, config.Get( 'commonapp_key' ) )
        self.CONFIG['key_auth'] = config.Get( 'commonapp_key_auth' )
        self.CONFIG['username'] = config.Get( 'commonapp_user' )
        self.CONFIG['auth'] = config.Get( 'commonapp_auth' )
        self.CONFIG['port'] = config.Get( 'commonapp_port' )
        self.CONFIG['timeout'] = config.Get( 'commonapp_timeout' )
        self.CONFIG['debug'] = config.Get( 'debug' )     
        self.DEBUG = config.Get( 'debug' )
        self.PATH = config.Get( 'commonapp_path' )
        if override_date:
            self.STRTODAY = override_date
        else:
            self.STRTODAY = datetime.date.today().strftime( config.Get( 'commonapp_dateformat' ) )
        self.DEBUG = config.Get( 'debug' )
    
    
    def Retrieve( self ):
        loglines = []
        dlist = []
        sftp, cloglines = ConnectSFTP( self.CONFIG )
        loglines.extend( cloglines )
        if not sftp:
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
                if (self.STRTODAY in filename) and not ('.zip' in filename):
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