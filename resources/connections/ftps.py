import os
from datetime import datetime, date, timedelta
from ..common.remotesites import FTPS

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
        self.SOURCEFOLDER = settings.get( 'sourcefolder' )
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
        destination = os.path.join( self.DATAROOT, 'downloads' )
        return ftps.Download( destination=destination, filter=self.FILTER, path=self.REMOTEPATH  )


    def Upload( self, files ):
        ftps = FTPS( self.CONFIG )
        origin = os.path.join( self.DATAROOT, 'downloads' )
        path = '/'.join( [self.REMOTEPATH, self.SOURCEFOLDER] )
        return ftps.Upload( files=files, origin=origin, path=path )
