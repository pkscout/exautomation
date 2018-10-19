import os
from datetime import datetime, date, timedelta
from ..common.remotesites import FTPS

class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
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
        self.REMOTEPATH = settings.get( 'destpath', '' )
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
        ftps = FTPS( self.CONFIG )
        return ftps.Download( destination=os.path.join( self.DATAROOT, 'downloads' ), filter=self.FILEDATE, path=self.REMOTEPATH  )



    def Upload( self, files ):
        ftps = FTPS( self.CONFIG )
        return ftps.Upload( files=files, origin=os.path.join( self.DATAROOT, 'downloads' ), path=self.REMOTEPATH )
