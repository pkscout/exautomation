from ..common.remotesites import FTPS, parseSettings

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        self.REMOTEPATH = settings.get( 'path' )
        self.CONFIG = {}
        self.CONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONFIG['host'] = settings.get( 'host' )
        self.CONFIG['port'] = settings.get( 'port', 990 )
        self.CONFIG['username'] = settings.get( 'user' )
        self.CONFIG['auth'] = settings.get( 'auth' )
        self.CONFIG['passive'] = settings.get( 'passive', False )
        self.CONFIG['authtls'] = settings.get( 'authtls', True )
        self.CONFIG['ssl'] = settings.get( 'ssl', False )
        self.CONFIG['debug'] = config.Get( 'debug' )


    def Download( self ):
        ftps = FTPS( self.CONFIG )
        return ftps.Download( destination=self.LOCALDOWNLOADPATH, filter=self.REMOTEFILTER, path=self.REMOTEPATH  )


    def Upload( self, files ):
        ftps = FTPS( self.CONFIG )
        return ftps.Upload( files=files, origin=self.LOCALDOWNLOADPATH, path='/'.join( [self.REMOTEPATH, self.SOURCEFOLDER] ) )
