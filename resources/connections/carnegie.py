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
        self.FILTER = filedate
        
        
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
            name = 'PCU-%s.csv' % self.FILTER
            if data == name:
                self.LATESTLINK = self.TESTLINK


    def handle_endtag(self, tag):
        if tag == "a":
            self.EXTRACTING = False
            self.TESTLINK = ''



class Connection:
    def __init__( self, config, settings ):
        self.DATAROOT = settings.get( 'dataroot' )
        if settings.get( 'override_date' ):
            dateformat = config.Get( 'override_dateformat' )
        else:
            dateformat = settings.get( 'dateformat', config.Get( 'override_dateformat' ) )
        thedate = settings.get( 'override_date', settings.get( 'filter' ) )
        try:
            self.FILTER = datetime.strptime( thedate, dateformat ).date()
        except TypeError as e:
            self.FILTER = (date.today() - timedelta( 1 )).strftime( dateformat )
        except ValueError as e:        
            self.FILTER = thedate
        self.PAYLOAD = { 'email': settings.get( 'user' ),
                    'password': settings.get( 'auth' ) }
        self.BASEURL = settings.get( 'host', config.Get( 'carnegie_baseURL' ) )
        self.CONNURL =  self.BASEURL + settings.get( 'path', config.Get( 'carnegie_path' ) )
        self.DEBUG = config.Get( 'debug' )

        
    def Download( self ):
        loglines = []
        with requests.Session() as s:
            loglines.append( 'attempting to get file from Carnegie server' )
            p = s.post( self.CONNURL, data = self.PAYLOAD )
            parser = cparser( self.FILTER )
            parser.feed( p.text )
            if parser.LATESTLINK:
                loglines.append( 'getting ' + parser.LATESTLINK )
                destfile = 'PCU-%s.csv' % self.FILTER
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
