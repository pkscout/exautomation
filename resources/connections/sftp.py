from ..common.remotesites import SFTP, parseSettings

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        self.REMOTEPATH = settings.get( 'path' )
        self.CONNECTCONFIG = {}
        self.CONNECTCONFIG['debug'] = config.Get( 'debug' )     
        self.CONNECTCONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONNECTCONFIG['hostkey'] = defaults.get( 'hostkey' )
        self.CONNECTCONFIG['host'] = settings.get( 'host' )
        self.CONNECTCONFIG['privatekey'] = defaults.get( 'privatekey' )
        self.CONNECTCONFIG['key_auth'] = settings.get( 'key_auth' )
        self.CONNECTCONFIG['username'] = settings.get( 'user' )
        self.CONNECTCONFIG['auth'] = settings.get( 'auth' )
        self.CONNECTCONFIG['port'] = settings.get( 'port', 22 )
        self.CONNECTCONFIG['timeout'] = settings.get( 'timeout', 15000 )
    
    
    def Download( self ):
        sftp = SFTP( self.CONNECTCONFIG )
        return sftp.Download( destination=self.LOCALDOWNLOADPATH, filter=self.REMOTEFILTER, path=self.REMOTEPATH  )
        

    def Upload( self, files ):
        sftp = SFTP( self.CONNECTCONFIG )
        return sftp.Upload( files=files, origin=self.LOCALDOWNLOADPATH, path='/'.join( [self.REMOTEPATH, self.SOURCEFOLDER] ) )
