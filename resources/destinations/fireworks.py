import chilkat, csv, os, ssl
from ..common.remotesites import FTPS

class Destination:
    def __init__( self, dataroot, config, source ):
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
        self.DESTPATH = config.Get( '%s_fireworks_path' % source )
        self.SOURCE = source
        self.DEBUG = config.Get( 'debug' )


    def Send( self, files ):
        fireworks = FTPS( self.CONFIG )
        return fireworks.Upload( files=files, origin=os.path.join( self.DATAROOT, 'downloads' ), path=self.DESTPATH )


    def Transform( self, files ):
        try:
            transform = getattr( self, '_' + self.SOURCE )
        except AttributeError:
            return files, ['no transformation needed, returning original file list']
        else:
            return transform( files )
    
    
    def _carnegie( self, files ):
        t_files = []
        loglines = []
        for file in files:
            orgfile = os.path.join( self.DATAROOT, 'downloads', file )
            destfilename = '%s-converted%s' % os.path.splitext( file )
            destfile = os.path.join( self.DATAROOT, 'downloads', destfilename )
            loglines.append( 'attempting to convert file' )
            loglines.append( 'opening %s' % orgfile )
            with open( orgfile,"r" ) as source:
                rdr= csv.reader( source )
                with open( destfile, "w" ) as result:
                    wtr = csv.writer( result )
                    loglines.append( 'removing bad last column from csv' )
                    for r in rdr:
                        del r[-1]
                        wtr.writerow( r )
            loglines.append( 'writing to ' + destfile )
            loglines.append( 'conversion complete' )
            tfiles.append( destfilename )
        return tfiles, loglines


    def _commonapp( self, files):
        csv_files = []
        loglines = []
        for file in files:
            if self.DEBUG:
                loglines.append( 'checking file ' + file )
            if '.csv' in file:
                loglines.append( 'adding %s to upload list' % file )
                csv_files.append( file )
        if not csv_files:
            loglines.append( 'no csv files in the Common App file download today' )
        return csv_files, loglines