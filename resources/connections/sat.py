import json, os, sys
from ..common.remotesites import parseSettings
from ..common.url import URL
from ..common.fileops import writeFile

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        self.REMOTEPATH = settings.get( 'path' )
        self.JSONURL = URL( 'json', {'Accept':'application/json', 'Content-Type': 'application/json'} )
        self.TEXTURL = URL( 'text' )
        self.ZIPURL = URL( 'binary' )
        baseURL = settings.get( 'host', config.Get( 'sat_baseURL' ) )
        self.LISTURL = baseURL + settings.get( 'list_path', config.Get( 'sat_list_path' ) )
        self.FILEURL = baseURL + settings.get( 'file_path', config.Get( 'sat_file_path' ) )
        payload = {}
        payload['username'] = settings.get( 'user' )
        payload['password'] = settings.get( 'auth' )
        self.PAYLOAD = json.dumps( payload )
        self.DEBUG = config.Get( 'debug' )

    
    def Download( self ):
        loglines = []
        url_params = {}
        dlist = []
        if self.REMOTEFILTER != 'all':
            url_params['fromDate'] = self.REMOTEFILTER
            loglines.append( 'getting SAT files newer than ' + self.REMOTEFILTER )
        else:
            loglines.append( 'getting all SAT files' )        
        success, uloglines, json_data = self.JSONURL.Post( self.LISTURL, params=url_params, data=self.PAYLOAD )
        if self.DEBUG:
            loglines.extend( uloglines )
        if success:
            if json_data['files'] is None:
                loglines.append( 'no SAT files to download today' )
                return False, loglines
            else:
                filequeue = []
                for file in json_data['files']:
                    filequeue.append( file['fileName'] )
                if not filequeue:
                    loglines.append( 'No SAT files to download today' )
                    return False, loglines
                for file in filequeue:
                    url_params = {}
                    url_params['filename'] = file
                    loglines.append( 'getting URL for file ' + file )
                    success, uloglines, file = self.JSONURL.Post( self.FILEURL, params=url_params, data=self.PAYLOAD )
                    if self.DEBUG:
                        loglines.extend( uloglines )
                    try:
                        loglines.append( 'retrieving file from ' + file['fileUrl'] )
                    except TypeError:
                        loglines.append( 'file is not json data, aborting' )
                        return False, loglines
                    if '.zip' in file['fileName']:
                        success, uloglines, urldata = self.ZIPURL.Get( file['fileUrl'] )
                        writetype = 'wb'                        
                    else:
                        success, uloglines, urldata = self.TEXTURL.Get( file['fileUrl'] )
                        writetype = 'w'
                    if self.DEBUG:
                        loglines.extend( uloglines )
                    loglines.append( 'saving file ' + file['fileName'] )
                    success, wloglines = writeFile( urldata, os.path.join( self.LOCALDOWNLOADPATH, file['fileName'] ), writetype )
                    if self.DEBUG:
                        loglines.extend( wloglines )
                    dlist.append( file['fileName'] )
                return dlist, loglines
        return False, loglines
        
        
    def Upload( self, files ):
        return False, ['Upload not implemented for SAT module']
