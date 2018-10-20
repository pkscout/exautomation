# *  Credits:
# *
# *  v.1.0.0
# *  original exautomation code by Kyle Johnson

import atexit, argparse, os, pathlib, random, re, sys, time
import data.config as config
from resources.common.xlogger import Logger
from resources.common.fileops import checkPath, deleteFile, renameFile, writeFile
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
        filter = self._parse_items( filters ).get( self.ARGS.source )
        if not filter:
            lw.log( ['no filters needed for source ' + self.ARGS.source], 'info' )
            return files
        ffiles = []
        for file in files:
            if re.search( filter, file ):
                ffiles.append( file )
        if ffiles:
            lw.log( ['no files remaining to process after running filter ' + filter], 'info' )
        return ffiles


    def _init_vars( self ):
        self.DATAROOT = os.path.join( p_folderpath, 'data' )
        thedirs = ['keys', 'downloads']
        for onedir in thedirs:
            exists, loglines = checkPath( os.path.join( self.DATAROOT, onedir, '' ) )
            lw.log( loglines )
        for source in config.Get( 'sources' ):
            if source['name'] == self.ARGS.source:
                settings = source
                break
        if self.ARGS.filter:
            settings['override_date'] = self.ARGS.filter
        settings['dataroot'] = self.DATAROOT
        try:
            self.SOURCE = connection_modules[settings['type']].Connection( config, settings )
        except UnboundLocalError as e:
            lw.log( ['no module matching %s found' % self.ARGS.source], 'info' )
            return False
        settings_list = []
        for destination in config.Get( 'destinations' ):
            if destination['name'] in self.ARGS.destination:
                settings_list.append( destination )
        self.DESTINATIONS = []
        for settings in settings_list:
            settings['sourcefolder'] = self.ARGS.source
            settings['override_date'] = self.ARGS.filter
            settings['dataroot'] = self.DATAROOT
            self.DESTINATIONS.append( [connection_modules[settings['type']].Connection( config, settings ), settings] )
        return True
        

    def _parse_argv( self ):
        parser = argparse.ArgumentParser()
        parser.add_argument( "-s", "--source", help="REQUIRED the external source", required=True )
        parser.add_argument( "-d", "--destination", help="REQUIRED the external destinations (destinations should be separated by a colon)", required=True )
        parser.add_argument( "-f", "--filter", help="overrides the default date behavior or source filter)" )
        self.ARGS = parser.parse_args()


    def _parse_items( self, items ):
        items_dict = {}
        if not items:
            return {}
        itemlist = items.split( ',' )
        for item in itemlist:
            item_parts = item.split(':')
            items_dict[item_parts[0].strip()] = item_parts[1].strip()
        return items_dict


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
        transforms = destconfig.get( 'transforms' )
        tfiles = []
        if not transforms:
            return files
        transform = self._parse_items( transforms ).get( self.ARGS.source )
        if not transform:
            lw.log( ['no transformation needed for %s when sending to %s' % (self.ARGS.source, destconfig.get( 'name',  ''))], 'info' )
            return files
        lw.log( ['transforming files using %s transform' % transform], 'info' )
        for file in files:
            destfile = os.path.join( self.DATAROOT, 'downloads', file )
            orgfilename = '%s-org%s' % os.path.splitext( file )
            orgfile = os.path.join( self.DATAROOT, 'downloads', orgfilename )
            success, loglines = renameFile( destfile, orgfile )
            lw.log( loglines )
            if not success:
                lw.log( ['error renaming %s to %s' % (destfile, orgfile)], 'info' )
                return False
            tfile, loglines = transform_modules[transform].Transform().Run( orgfile, destfile, destconfig.get( '%s_%s_config' % (self.ARGS.source, transform), {} ) )
            lw.log( loglines )
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