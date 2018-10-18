import os, sys
from datetime import datetime, date, timedelta
from ..common.remotesites import SFTP

class Source:
    def __init__( self, dataroot, config, override_date ):
        self.DATAROOT = dataroot
        self.CONFIG = {}
        self.CONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONFIG['module_name'] = 'Common App SFTP'
        self.CONFIG['hostkey'] = os.path.join( dataroot, 'keys', 'commonapp_host.key' )
        self.CONFIG['host'] = config.Get( 'commonapp_baseURL' )
        self.CONFIG['privatekeypath'] = os.path.join( dataroot, 'keys', 'commonapp_private.key' )
        self.CONFIG['key_auth'] = config.Get( 'commonapp_key_auth' )
        self.CONFIG['username'] = config.Get( 'commonapp_user' )
        self.CONFIG['auth'] = config.Get( 'commonapp_auth' )
        self.CONFIG['port'] = config.Get( 'commonapp_port' )
        self.CONFIG['timeout'] = config.Get( 'commonapp_timeout' )
        self.CONFIG['debug'] = config.Get( 'debug' )     
        self.REMOTEPATH = config.Get( 'commonapp_path' )
        if override_date:
            try:
                filedate = datetime.strptime( override_date, config.Get( 'override_dateformat' ) ).date()
            except ValueError as e:
                print( 'Error: ' + str( e ) )
                raise ValueError( str( e ) )
        else:
            filedate = date.today() - timedelta(1)
        self.FILEDATE = filedate.strftime( config.Get( 'commonapp_dateformat' ) )
    
    
    def Retrieve( self ):
        commonapp = SFTP( self.CONFIG )
        return commonapp.Download( destination=os.path.join( self.DATAROOT, 'downloads' ), filter=self.FILEDATE, path=self.REMOTEPATH  )