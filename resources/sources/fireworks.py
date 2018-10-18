import os
from datetime import datetime, date, timedelta
from ..common.remotesites import FTPS

class Source:
    def __init__( self, dataroot, config, override_date ):
        self.DATAROOT = dataroot
        self.CONFIG = {}
        self.CONFIG['chilkat_license'] = config.Get( 'chilkat_license' )
        self.CONFIG['module_name'] = 'Fireworks FTPS'
        self.CONFIG['host'] = config.Get( 'fireworks_baseURL' )
        self.CONFIG['port'] = config.Get( 'fireworks_port' )
        self.CONFIG['username'] = config.Get( 'fireworks_user' )
        self.CONFIG['auth'] = config.Get( 'fireworks_auth' )
        self.CONFIG['ftps_passive'] = True
        self.CONFIG['ftps_authtls'] = False
        self.CONFIG['ftps_ssl'] = True
        self.CONFIG['debug'] = config.Get( 'debug' )
        self.REMOTEPATH = config.Get( 'fireworks_source_path' )
        if override_date:
            try:
                filedate = datetime.strptime( override_date, config.Get( 'override_dateformat' ) ).date()
            except ValueError as e:
                print( 'Error: ' + str( e ) )
                raise ValueError( str( e ) )
        else:
            filedate = date.today() - timedelta(1)
        self.FILEDATE = filedate.strftime( config.Get( 'fireworks_dateformat' ) )


    def Retrieve( self ):
        fireworks = FTPS( self.CONFIG )
        return fireworks.Download( destination=os.path.join( self.DATAROOT, 'downloads' ), filter=self.FILEDATE, path=self.REMOTEPATH  )