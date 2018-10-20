import os
from datetime import datetime, date, timedelta
from ..common.remotesites import SFTP

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
        self.CONFIG['debug'] = config.Get( 'debug' )     
        self.CONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONFIG['hostkey'] = os.path.join( settings.get( 'dataroot' ), 'keys', settings.get( 'name' ) + '_host.key' )
        self.CONFIG['host'] = settings.get( 'host' )
        self.CONFIG['privatekeypath'] = os.path.join( settings.get( 'dataroot' ), 'keys', settings.get( 'name' ) + '_private.key' )
        self.CONFIG['key_auth'] = settings.get( 'key_auth' )
        self.CONFIG['username'] = settings.get( 'user' )
        self.CONFIG['auth'] = settings.get( 'auth' )
        self.CONFIG['port'] = settings.get( 'port', 22 )
        self.CONFIG['timeout'] = settings.get( 'timeout', 15000 )
    
    
    def Download( self ):
        sftp = SFTP( self.CONFIG )
        destination = os.path.join( self.DATAROOT, 'downloads' )
        return sftp.Download( destination=destination, filter=self.FILTER, path=self.REMOTEPATH  )
        

    def Upload( self, files ):
        sftp = SFTP( self.CONFIG )
        origin = os.path.join( self.DATAROOT, 'downloads' )
        path = '/'.join( [self.REMOTEPATH, self.SOURCEFOLDER] )
        return sftp.Upload( files=files, origin=origin, path=path )
