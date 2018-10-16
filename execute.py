# *  Credits:
# *
# *  v.0.3.0
# *  original exautomation code by Kyle Johnson

import atexit, argparse, importlib, os, random, subprocess, sys, time
import data.config as config
from resources.common.xlogger import Logger
from resources.common.fileops import writeFile, deleteFile, checkPath
if sys.version_info < (3, 0):
    from ConfigParser import *
else:
    from configparser import *

p_folderpath, p_filename = os.path.split( os.path.realpath(__file__) )
checkPath( os.path.join( p_folderpath, 'data', 'logs', '' ) )
lw = Logger( logfile = os.path.join( p_folderpath, 'data', 'logs', 'logfile.log' ),
             numbackups = config.Get( 'logbackups' ), logdebug = str( config.Get( 'debug' ) ) )

def _deletePID():
    success, loglines = deleteFile( pidfile )
    lw.log (loglines )

pid = str(os.getpid())
pidfile = os.path.join( p_folderpath, 'data', 'adm_auto.pid' )
atexit.register( _deletePID )

class Main:
    def __init__( self ):
        self._setPID()
        self._parse_argv()
        success = self._init_vars()
        if not success:
            lw.log( ['required modules could not be loaded, exiting'], 'info' )
            return
        self._trim_downloads()
        rfiles, loglines = self.SOURCE.Retrieve() 
        lw.log( loglines, 'info' )       
        if not rfiles:
            lw.log( ['files could not be retrieved for source %s, exiting'  % self.ARGS.source], 'info' )
            return
        tfiles, loglines = self.DESTINATION.Transform( rfiles )
        lw.log( loglines, 'info' )
        if not tfiles:
            lw.log( ['files could not be transformed for source %s, exiting'  % self.ARGS.source], 'info' )
            return
        success, loglines = self.DESTINATION.Send( tfiles )
        lw.log( loglines, 'info' )
        if success:
            lw.log( ['files successfully transfered to destination %s, exiting'  % self.ARGS.destination], 'info' )
        else:
            lw.log( ['files failed to transfer to destination %s, exiting'  % self.ARGS.destination], 'info' )        


    def _init_vars( self ):
        self.DATAROOT = os.path.join( p_folderpath, 'data' )
        thedirs = ['keys', 'downloads']
        for onedir in thedirs:
            exists, loglines = checkPath( os.path.join( self.DATAROOT, onedir, '' ) )
            lw.log( loglines )
        try:
            sourcemodule = importlib.import_module( "resources.sources." + self.ARGS.source )
        except ImportError as e:
            sourcemodule = False
            lw.log( ['module for source %s could not be loaded' % self.ARGS.source, e], 'info' )
        try:
            destmodule = importlib.import_module( "resources.destinations." + self.ARGS.destination )
        except ImportError as e:
            destmodule = False
            lw.log( ['module for destination %s could not be loaded' % self.ARGS.destination, e], 'info' )
        if (not sourcemodule) or (not destmodule):
            return False
        self.SOURCE = sourcemodule.Source( self.DATAROOT, config, self.ARGS.date )
        self.DESTINATION = destmodule.Destination( self.DATAROOT, config, self.ARGS.source )
        return True
        

    def _parse_argv( self ):
        parser = argparse.ArgumentParser()
        parser.add_argument( "-s", "--source", help="REQUIRED the external source (carnegie, act, sat, commonapp)", required=True )
        parser.add_argument( "-d", "--destination", help="REQUIRED the external destination (fireworks)", required=True )
        parser.add_argument( "-t", "--date", help="override default behavior of now (format will depend on source)" )
        self.ARGS = parser.parse_args()


    def _setPID( self ):
        while os.path.isfile( pidfile ):
            time.sleep( random.randint( 1, 3 ) )
            if time.time() - basetime > config.Get( 'aborttime' ):
                err_str = 'taking too long for previous process to finish - aborting attempt to run automation'
                lw.log( [err_str], 'info' )
                sys.exit( err_str )
        lw.log( ['setting PID file'] )
        success, loglines = writeFile( pid, pidfile, wtype='w' )
        lw.log( loglines )        


    def _trim_downloads( self ):
        download_max = config.Get( 'download_max' )
        if download_max:
            download_path = os.path.join( self.DATAROOT, 'downloads')
            download_max = download_max*1024000
            total_size = 0
            filelist = []
            for dirpath, dirnames, filenames in os.walk( download_path ):
                for file in filenames:
                    filepath = os.path.join( dirpath, file )
                    filelist.append( filepath )
                    total_size += os.path.getsize( filepath )
            if total_size > download_max:
                lw.log( ['trimming the download folder down to %s bytes' % download_max], 'info'  )
                try:
                    filelist.sort( key=lambda x: os.path.getmtime( x ) )
                except Exception as e:
                    lw.log( ['unexpected error sorting download directory', e], 'info' )
                    return
                for file in filelist:
                    if( total_size > download_max ):
                        total_size = total_size - os.path.getsize( file )
                        success, dloglines = deleteFile( file )
                        lw.log( dloglines, 'info' )
                    else:
                        break



if ( __name__ == "__main__" ):
    lw.log( ['script started'], 'info' )
    Main()
lw.log( ['script finished'], 'info' )