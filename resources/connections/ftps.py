from resources.common.remotesites import FTPS, parseSettings

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        self.REMOTEPATH = settings.get( 'path', '' )
        self.CONNECTCONFIG = {}
        self.CONNECTCONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONNECTCONFIG['host'] = settings.get( 'host' )
        self.CONNECTCONFIG['port'] = settings.get( 'port', 990 )
        self.CONNECTCONFIG['username'] = settings.get( 'user' )
        self.CONNECTCONFIG['auth'] = settings.get( 'auth' )
        self.CONNECTCONFIG['passive'] = settings.get( 'passive', False )
        self.CONNECTCONFIG['authtls'] = settings.get( 'authtls', True )
        self.CONNECTCONFIG['ssl'] = settings.get( 'ssl', False )
        self.CONNECTCONFIG['debug'] = config.Get( 'debug' )
        self.CONNECTCONFIG['deleteafterdownload'] = settings.get( 'deleteafterdownload' )


    def Download( self ):
        ftps = FTPS( self.CONNECTCONFIG )
        return ftps.Download( destination=self.LOCALDOWNLOADPATH, filter=self.REMOTEFILTER, path=self.REMOTEPATH  )


    def Upload( self, files ):
        ftps = FTPS( self.CONNECTCONFIG )
        return ftps.Upload( files=files, origin=self.LOCALDOWNLOADPATH, path='/'.join( [self.REMOTEPATH, self.SOURCEFOLDER] ) )
