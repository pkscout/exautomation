from ..remotesites import SMB, parseSettings

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        self.REMOTEPATH = settings.get( 'path' )
        self.CONNECTCONFIG = {}
        self.CONNECTCONFIG['debug'] = config.Get( 'debug' )     
        self.CONNECTCONFIG['host'] = settings.get( 'host' )
        self.CONNECTCONFIG['hostip'] = settings.get( 'hostip' )
        self.CONNECTCONFIG['user'] = settings.get( 'user' )
        self.CONNECTCONFIG['auth'] = settings.get( 'auth' )
        self.CONNECTCONFIG['clientname'] = settings.get( 'clientname' )
        self.CONNECTCONFIG['share'] = settings.get( 'share' )
        self.CONNECTCONFIG['port'] = settings.get( 'port', 445 )
        self.CONNECTCONFIG['domainname'] = settings.get( 'domainname', '' )
        self.CONNECTCONFIG['usentlmv2'] = settings.get( 'usentlmv2', True )
        self.CONNECTCONFIG['isdirectip'] = settings.get( 'usedirectip', True )
    
    
    def Download( self ):
        smb = SMB( self.CONNECTCONFIG )
        return smb.Download( destination=self.LOCALDOWNLOADPATH, filter=self.REMOTEFILTER, path=self.REMOTEPATH  )
        

    def Upload( self, files ):
        smb = SMB( self.CONNECTCONFIG )
        return smb.Upload( files=files, origin=self.LOCALDOWNLOADPATH, path='/'.join( [self.REMOTEPATH, self.SOURCEFOLDER] ) )
