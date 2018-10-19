import os, requests, shutil
from datetime import datetime, date, timedelta
from html.parser import HTMLParser

class cparser( HTMLParser ):
    def __init__( self, filedate ):
        super().__init__()
        self.reset()
        self.EXTRACTING = False
        self.TESTLINK = ''
        self.LATESTLINK = ''
        self.FILEDATE = filedate
        
        
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d_attrs = dict(attrs)
            try:
                self.TESTLINK = d_attrs["href"]
            except TypeError:
                self.TESTLINK = ''
            self.EXTRACTING = True


    def handle_data( self, data ):
        if self.EXTRACTING:
            name = 'PCU-%s.csv' % self.FILEDATE
            if data == name:
                self.LATESTLINK = self.TESTLINK


    def handle_endtag(self, tag):
        if tag == "a":
            self.EXTRACTING = False
            self.TESTLINK = ''



class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
        self.PAYLOAD = { 'email': settings.get( 'user' ),
                    'password': settings.get( 'auth' ) }
        self.BASEURL = settings.get( 'host', config.Get( 'carnegie_baseURL' ) )
        self.CONNURL =  self.BASEURL + settings.get( 'path', config.Get( 'carnegie_path' ) )
        self.DEBUG = config.Get( 'debug' )
        if settings.get( 'override_date' ) and settings.get( 'override_date' ) != 'all':
            try:
                filedate = datetime.strptime( settings.get( 'override_date' ), config.Get( 'override_dateformat' ) ).date()
            except ValueError as e:
                print( 'Error: ' + str( e ) )
                raise ValueError( str( e ) )
        else:
            filedate = date.today() - timedelta(1)
        self.FILEDATE = filedate.strftime( settings.get( 'dateformat', config.Get( 'dateformat' ) ) )

        
    def Download( self ):
        loglines = []
        with requests.Session() as s:
            loglines.append( 'attempting to get file from Carnegie server' )
            p = s.post( self.CONNURL, data = self.PAYLOAD )
            parser = cparser( self.FILEDATE )
            parser.feed( p.text )
            if parser.LATESTLINK:
                loglines.append( 'getting ' + parser.LATESTLINK )
                destfile = 'PCU-%s.csv' % self.FILEDATE
                dest = os.path.join( self.DATAROOT, 'downloads', destfile)
                rURL = self.BASEURL + parser.LATESTLINK + '?send=True'
                r = s.get( rURL, stream=True )
                if r.status_code == 200:
                    with open(dest, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    loglines.append( 'saved %s to %s' % (rURL, dest ) )
                    return [destfile], loglines
                else:
                    loglines.append( 'unable to save %s to %s' % (rURL, dest ) )
                    return False, loglines
            else:
                loglines.append( 'no file to get today' )
                return False, loglines


    def Upload( self, files ):
        return False, ['Upload not implemented for Carnegie module']
