# *  Credits:
# *
# *  v.0.1.0
# *  original adm_auto code by Kyle Johnson

import atexit, argparse, importlib, os, random, subprocess, sys, time
import data.config as config
from resources.common.xlogger import Logger
from resources.common.fileops import writeFile, deleteFile
if sys.version_info < (3, 0):
    from ConfigParser import *
else:
    from configparser import *

p_folderpath, p_filename = os.path.split( os.path.realpath(__file__) )
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
        dataroot = os.path.join( p_folderpath, 'data' )
        self.SOURCE = sourcemodule.Source( dataroot, config, self.ARGS.date )
        self.DESTINATION = destmodule.Destination( dataroot, config, self.ARGS.source )
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



if ( __name__ == "__main__" ):
    lw.log( ['script started'], 'info' )
    Main()
lw.log( ['script finished'], 'info' )