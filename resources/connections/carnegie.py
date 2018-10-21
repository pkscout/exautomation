import os, requests, shutil
from ..remotesites import parseSettings
from html.parser import HTMLParser

class cparser( HTMLParser ):
    def __init__( self, filedate ):
        super().__init__()
        self.reset()
        self.EXTRACTING = False
        self.TESTLINK = ''
        self.LATESTLINK = ''
        self.REMOTEFILTER = filedate
        
        
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
            name = 'PCU-%s.csv' % self.REMOTEFILTER
            if data == name:
                self.LATESTLINK = self.TESTLINK


    def handle_endtag(self, tag):
        if tag == "a":
            self.EXTRACTING = False
            self.TESTLINK = ''



class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.REMOTEPATH = settings.get( 'path' )
        self.SOURCEFOLDER = settings.get( 'sourcefolder' )
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
            parser = cparser( self.REMOTEFILTER )
            parser.feed( p.text )
            if parser.LATESTLINK:
                loglines.append( 'getting ' + parser.LATESTLINK )
                destfile = 'PCU-%s.csv' % self.REMOTEFILTER
                dest = os.path.join( self.LOCALDOWNLOADPATH, destfile)
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
