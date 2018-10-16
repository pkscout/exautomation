import chilkat, csv, os, ssl
from ..common.remotesites import ConnectFTPS

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
        loglines = []
        ftps, cloglines = ConnectFTPS( self.CONFIG )
        loglines.extend( cloglines )
        if not ftps:
            return False, loglines
        success = ftps.ChangeRemoteDir( self.DESTPATH )
        if (success != True):
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        loglines.append( 'setting destination directory to ' + self.DESTPATH )
        loglines.append( 'transferring files to Fireworks FTPS server' )
        fsuccess = True
        for file in files:        
            loglines.append( 'transferring file ' + file )
            filepath = os.path.join( self.DATAROOT, 'downloads', file )
            success = ftps.PutFile( filepath, file )
            if (success != True):
                loglines.append( ftps.lastErrorText() )
                fsuccess = False
        loglines.append( 'disconnecting from Fireworks FTPS server' )
        success = ftps.Disconnect()
        return fsuccess, loglines


    def Transform( self, files ):
        loglines = []
        tfiles = []
        if self.SOURCE == "carnegie":
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
        loglines.append( 'no transformation needed, returning original file list' )
        return files, loglines