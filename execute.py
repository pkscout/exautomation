# *  Credits:
# *
# *  v.1.3.1
# *  original exautomation code by Kyle Johnson

import atexit, argparse, os, pathlib, random, re, sys, time
import resources.config as config
from resources.common.xlogger import Logger
from resources.common.fileops import checkPath, deleteFile, renameFile, writeFile
from resources.common.remotesites import _parse_items
import resources.connections, resources.transforms
if sys.version_info < (3, 0):
    from ConfigParser import *
else:
    from configparser import *

p_folderpath, p_filename = os.path.split( os.path.realpath(__file__) )
checkPath( os.path.join( p_folderpath, 'data', 'logs', '' ) )
lw = Logger( logfile=os.path.join( p_folderpath, 'data', 'logs', 'logfile.log' ),
             logconfig='timed', numbackups=config.Get( 'logbackups' ), logdebug=str( config.Get( 'debug' ) ) )

connection_modules = {}
for module in resources.connections.__all__:
    full_plugin = 'resources.connections.' + module
    __import__( full_plugin )
    imp_plugin = sys.modules[ full_plugin ]
    lw.log( ['loaded plugin ' + module] )
    connection_modules[module] = imp_plugin
transform_modules = {}
for module in resources.transforms.__all__:
    full_plugin = 'resources.transforms.' + module
    __import__( full_plugin )
    imp_plugin = sys.modules[ full_plugin ]
    lw.log( ['loaded plugin ' + module] )
    transform_modules[module] = imp_plugin


def _deletePID():
    success, loglines = deleteFile( pidfile )
    lw.log (loglines )

pid = str(os.getpid())
pidfile = os.path.join( p_folderpath, 'data', 'exautomation.pid' )
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
        lw.log( ['attempting to retrieve files for source %s'  % self.ARGS.source], 'info' )
        rfiles, loglines = self.SOURCE.Download() 
        lw.log( loglines, 'info' )     
        if not rfiles:
            lw.log( ['no files retrieved'], 'info' )
            return
        for destination in self.DESTINATIONS:
            lw.log( ['filtering files'], 'info' )
            ffiles = self._filter_files( rfiles, destination[1].get( 'filters' ) )
            if not ffiles:
                return            
            if len( ffiles ) > 1 and destination[1].get( 'mergefiles', False ):
                lw.log( ['attempting to merge files from source %s for destination %s'  % (self.ARGS.source, destination[1].get( 'name', '' ))], 'info' )
                ffiles = self._merge_files( ffiles, destination[1].get( 'hasheaders', {} ).get( self.ARGS.source, True ) )
            lw.log( ['attempting to transform files from source %s for destination %s'  % (self.ARGS.source, destination[1].get( 'name', '' ))], 'info' )
            tfiles = self._transform_files( ffiles, destination[1] )
            if not tfiles:
                return
            lw.log( ['attempting to send files from source %s to destination %s'  % (self.ARGS.source, destination[1].get( 'name', '' ))], 'info' )
            success, loglines = destination[0].Upload( tfiles )
            lw.log( loglines, 'info' )


    def _filter_files( self, files, filters ):
        if not filters:
            return files
        filter = _parse_items( filters ).get( self.ARGS.source )
        if not filter:
            lw.log( ['no filters needed for source ' + self.ARGS.source], 'info' )
            return files
        ffiles = []
        for file in files:
            if re.search( filter, file ):
                ffiles.append( file )
        if not ffiles:
            lw.log( ['no files remaining to process after running filter ' + filter], 'info' )
        return ffiles


    def _init_vars( self ):
        self.DATAROOT = os.path.join( p_folderpath, 'data' )
        thedirs = ['keys', 'downloads']
        for onedir in thedirs:
            exists, loglines = checkPath( os.path.join( self.DATAROOT, onedir, '' ) )
            lw.log( loglines )
        settings = {}
        for source in config.Get( 'sources' ):
            if source['name'] == self.ARGS.source:
                settings = source
                break
        if not settings:
            lw.log( ['no matching source for ' + self.AGRGS.source], 'info' )
            return False
        if self.ARGS.filter:
            settings['override_date'] = self.ARGS.filter
        settings['dataroot'] = self.DATAROOT
        try:
            self.SOURCE = connection_modules.get( settings.get( 'type', 'NOTHING' ), 'NOTHING' ).Connection( config, settings )
        except UnboundLocalError as e:
            lw.log( ['no %s type module for source %s found' % (settings.get( 'type' ), self.ARGS.source)], 'info' )
            return False
        except AttributeError as e:
            lw.log( ['it looks like you either have no data/settings.py folder or it is malformed', e], 'info' )
            return False
        settings_list = []
        for destination in config.Get( 'destinations' ):
            if destination['name'] in self.ARGS.destination:
                settings_list.append( destination )
        self.DESTINATIONS = []
        for settings in settings_list:
            settings['sourcefolder_default'] = self.ARGS.source
            settings['override_date'] = self.ARGS.filter
            settings['dataroot'] = self.DATAROOT
            self.DESTINATIONS.append( [connection_modules[settings['type']].Connection( config, settings ), settings] )
        return True
        

    def _merge_files( self, files, hasheader):
        main = files.pop( 0 )
        dpath = os.path.join( self.DATAROOT, 'downloads' )
        with open( os.path.join( dpath, main ), 'a' ) as outfile:
            for file in files:
                with open( os.path.join( dpath, file ), 'r' ) as infile:
                    if hasheader:
                        header, data = infile.read().split('\n', 1)
                    else:
                        data = infile.read()
                    outfile.write( data )
        return [main]


    def _parse_argv( self ):
        parser = argparse.ArgumentParser()
        parser.add_argument( "-s", "--source", help="REQUIRED the external source", required=True )
        parser.add_argument( "-d", "--destination", help="REQUIRED the external destinations (destinations should be separated by a colon)", required=True )
        parser.add_argument( "-f", "--filter", help="overrides the default date behavior or source filter)" )
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


    def _transform_files( self, files, destconfig ):
        transforms_list = destconfig.get( 'transforms' )
        tfiles = []
        if not transforms_list:
            lw.log( ['no transformations listed for destination ' + destconfig.get( 'name',  '')], 'info' )
            return files
        transforms = _parse_items( transforms_list ).get( self.ARGS.source )
        if not transforms:
            lw.log( ['no transformations needed for %s when sending to %s' % (self.ARGS.source, destconfig.get( 'name',  ''))], 'info' )
            return files
        for transform in _parse_items( transforms, itemdelim=';', subitemdelim=None ):
            if tfiles:
                usefiles = tfiles
                tfiles = []
            else:
                usefiles = files
            lw.log( ['transforming files using %s transform' % transform], 'info' )
            for file in usefiles:
                destfile = os.path.join( self.DATAROOT, 'downloads', file )
                file_exists = True
                i = 1
                while file_exists:
                    filepieces = os.path.splitext( file )
                    orgfilename = '%s-org%s%s' % (filepieces[0], str( i ), filepieces[1])
                    orgfile = os.path.join( self.DATAROOT, 'downloads', orgfilename )
                    file_exists = os.path.isfile( orgfile )
                    i = i + 1
                success, loglines = renameFile( destfile, orgfile )
                lw.log( loglines )
                if not success:
                    lw.log( ['error renaming %s to %s' % (destfile, orgfile)], 'info' )
                    return False
                try:
                    tfile, loglines = transform_modules[transform].Transform().Run( orgfile, destfile, destconfig.get( '%s_%s_config' % (self.ARGS.source, transform), {} ), config.Get( 'debug' ) )
                except KeyError as e:
                    lw.log( ['no transform module named %s found' % transform], 'info' )
                    return False
                lw.log( loglines, 'info' )
                if tfile:
                    tpath = pathlib.PurePath( tfile )
                    tfiles.append( tpath.name )
                else:
                    lw.log( ['error transforming file ' + file], 'info' )
        return tfiles


    def _trim_downloads( self ):
        download_max = config.Get( 'download_max' )
        if download_max:
            download_path = os.path.join( self.DATAROOT, 'downloads')
            download_max = download_max*1024*1024
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