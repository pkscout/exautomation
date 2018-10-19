import os
from datetime import datetime, date, timedelta
from ..common.remotesites import SFTP

class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
        self.CONFIG = {}
        self.CONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONFIG['hostkey'] = os.path.join( settings.get( 'dataroot' ), 'keys', settings.get( 'name' ) + '_host.key' )
        self.CONFIG['host'] = settings.get( 'host' )
        self.CONFIG['privatekeypath'] = os.path.join( settings.get( 'dataroot' ), 'keys', settings.get( 'name' ) + '_private.key' )
        self.CONFIG['key_auth'] = settings.get( 'key_auth' )
        self.CONFIG['username'] = settings.get( 'user' )
        self.CONFIG['auth'] = settings.get( 'auth' )
        self.CONFIG['port'] = settings.get( 'port', 22 )
        self.CONFIG['timeout'] = settings.get( 'timeout', 15000 )
        self.CONFIG['debug'] = config.Get( 'debug' )     
        self.REMOTEPATH = settings.get( 'path', '.' )
        if settings.get( 'override_date' ) and settings.get( 'override_date' ) != 'all':
            try:
                filedate = datetime.strptime( settings.get( 'override_date' ), config.Get( 'override_dateformat' ) ).date()
            except ValueError as e:
                print( 'Error: ' + str( e ) )
                raise ValueError( str( e ) )
        else:
            filedate = date.today() - timedelta(1)
        self.FILEDATE = filedate.strftime( settings.get( 'dateformat', config.Get( 'dateformat' ) ) )
    
    
    def Download( self ):
        sftp = SFTP( self.CONFIG )
        return sftp.Download( destination=os.path.join( self.DATAROOT, 'downloads' ), filter=self.FILEDATE, path=self.REMOTEPATH  )
        

    def Upload( self, files ):
        sftp = SFTP( self.CONFIG )
        return sftp.Upload( files=files, origin=os.path.join( self.DATAROOT, 'downloads' ), path=self.REMOTEPATH )
