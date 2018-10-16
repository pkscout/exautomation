import datetime, json, os, sys
from ..common.url import URL
from ..common.fileops import writeFile

class Source:
    def __init__( self, dataroot, config, override_date ):
        self.DATAROOT = dataroot
        self.JSONURL = URL( 'json', {'Accept':'application/json', 'Content-Type': 'application/json'} )
        self.TEXTURL = URL( 'text' )
        self.LISTURL = config.Get( 'sat_baseURL' ) + config.Get( 'sat_list_path' )
        self.FILEURL = config.Get( 'sat_baseURL' ) + config.Get( 'sat_file_path' )
        payload = {}
        payload['username'] = config.Get( 'sat_user' )
        payload['password'] = config.Get( 'sat_auth' )
        self.PAYLOAD = json.dumps( payload )
        self.DEBUG = config.Get( 'debug' )
        if override_date:
            if override_date == 'all':
                self.FROMDATE = None
                return
            else:
                fromdate = datetime.strptime( override_date, config.Get( 'override_dateformat' ) ).date()
        else:
            fromdate = datetime.date.today() - datetime.timedelta(1)
        self.FROMDATE = fromdate.strftime( config.Get( 'sat_dateformat' ) + config.Get( 'gmtoffset' ) )

    
    def Retrieve( self ):
        loglines = []
        url_params = {}
        dlist = []
        if self.FROMDATE:
            url_params['fromDate'] = self.FROMDATE
            loglines.append( 'getting SAT files newer than ' + self.FROMDATE )
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
                    if file['fileType'] == 'Scores File':
                        filequeue.append( file['fileName'] )
                if not filequeue:
                    loglines.append( 'No SAT Score Files to download today' )
                    return False, loglines
                downloadqueue = []
                for file in filequeue:
                    url_params = {}
                    url_params['filename'] = file
                    loglines.append( 'getting URL for file ' + file )
                    success, uloglines, json_data = self.JSONURL.Post( self.FILEURL, params=url_params, data=self.PAYLOAD )
                    if self.DEBUG:
                        loglines.extend( uloglines )
                    downloadqueue.append( json_data )
                for file in downloadqueue:
                    loglines.append( 'retrieving file from ' + file['fileUrl'] )
                    success, uloglines, urldata = self.TEXTURL.Get( file['fileUrl'] )
                    if self.DEBUG:
                        loglines.extend( uloglines )
                    loglines.append( 'saving file ' + file['fileName'] )
                    success, wloglines = writeFile( urldata, os.path.join( self.DATAROOT, 'downloads', file['fileName'] ), 'w' )
                    if self.DEBUG:
                        loglines.extend( wloglines )
                    dlist.append( file['fileName'] )
                return dlist, loglines
        return False, loglines