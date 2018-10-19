import json, os, sys
from datetime import datetime, date, timedelta
from ..common.url import URL
from ..common.fileops import writeFile

class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
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
        if settings.get( 'override_date'):
            if settings.get( 'override_date' ) == 'all':
                self.FILEDATE = None
                return
            try:
                filedate = datetime.strptime( settings.get( 'override_date' ), config.Get( 'override_dateformat' ) ).date()
            except ValueError as e:
                print( 'Error: ' + str( e ) )
                raise ValueError( str( e ) )
        else:
            filedate = date.today() - timedelta(1)
        self.FILEDATE = filedate.strftime( settings.get( 'dateformat', config.Get( 'sat_dateformat' ) ) + config.Get( 'gmtoffset' ) )

    
    def Download( self ):
        loglines = []
        url_params = {}
        dlist = []
        if self.FILEDATE:
            url_params['fromDate'] = self.FILEDATE
            loglines.append( 'getting SAT files newer than ' + self.FILEDATE )
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
                    success, wloglines = writeFile( urldata, os.path.join( self.DATAROOT, 'downloads', file['fileName'] ), writetype )
                    if self.DEBUG:
                        loglines.extend( wloglines )
                    dlist.append( file['fileName'] )
                return dlist, loglines
        return False, loglines