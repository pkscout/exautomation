import os

class Destination:
    def __init__( self, dataroot, config, source ):
        self.DATAROOT = dataroot
        self.DESTPATH = config.Get( '%s_local_path' % source )
        self.SOURCE = source
        self.DEBUG = config.Get( 'debug' )


    def Send( self, files ):
        return (True, ['No action just testing.'])


    def Transform( self, files ):
        try:
            transform = getattr( self, '_' + self.SOURCE )
        except AttributeError:
            return files, ['no transformation needed, returning original file list']
        else:
            return transform( files )