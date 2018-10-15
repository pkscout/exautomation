import chilkat, csv, os, ssl

class Destination:
    def __init__( self, dataroot, config, source ):
        self.DATAROOT = dataroot
        self.CHILKATLICENSE = config.Get( 'chilkat_license' )
        self.SOURCE = source
        self.DESTPATH = config.Get( '%s_fireworks_path' % source )
        self.HOST = config.Get( 'fireworks_baseURL' )
        self.PORT = config.Get( 'fireworks_port' )
        self.USERNAME = config.Get( 'fireworks_user' )
        self.AUTH = config.Get( 'fireworks_auth' )
        self.DEBUG = config.Get( 'debug' )


    def Send( self, files ):
        loglines = []
        ftps = chilkat.CkFtp2()
        success = sftp.UnlockComponent( self.CHILKATLICENSE )
        if (success != True):
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        loglines.append( 'connecting to Fireworks FTPS server' )
        ftps.put_Passive(True)
        ftps.put_Hostname( self.HOST )
        ftps.put_Username( self.USERNAME )
        ftps.put_Password( self.AUTH )
        ftps.put_Port( self.PORT )
        ftps.put_AuthTls( False )
        ftps.put_Ssl( True )
        success = ftps.Connect()
        if (success != True):
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        elif self.DEBUG:
            loglines.extend( [ftps.lastErrorText(), 'ftps channel established!'] )
        success = ftps.ChangeRemoteDir( self.DESTPATH )
        if (success != True):
            loglines.append( ftps.lastErrorText() )
            return False, loglines
        loglines.append( 'setting destination directory to ' + self.DESTPATH )
        loglines.append( 'transferring files to Fireworks FTPS server' )
        for file in files:        
            loglines.append( 'transferring file ' + file )
            filepath = os.path.join( self.DATAROOT, file )
            success = ftps.PutFile( filepath, file )
            if (success != True):
                loglines.append( ftps.lastErrorText() )
            else:
                loglines.append( 'deleting ' + filepath )
                os.remove( filepath )
        loglines.append( 'disconnecting from Fireworks FTPS server' )
        success = ftps.Disconnect()
        return True, loglines


    def Transform( self, files ):
        loglines = []
        tfiles = []
        if self.SOURCE == "carnegie":
            for file in files:
                orgfile = os.path.join( self.DATAROOT, file )
                destfilename = '%s-converted%s' % os.path.splitext( file )
                destfile = os.path.join( self.DATAROOT, destfilename )
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
                loglines.append( 'deleting ' + orgfile )
                os.remove( orgfile )
                loglines.append( 'conversion complete' )
                tfiles.append( destfilename )
            return tfiles, loglines
        loglines.append( 'no transformation needed, returning original file list' )
        return files, loglines