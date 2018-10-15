# exautomation
Python command line tool to automate various file exchanges


PREREQUISITES:
Python 3.x (tested with Python 3.7, might work with Python 2.x, but I doubt it)
requests module (pip3 install requests)
chilkat module (download/purchase from http://www.chilkatsoft.com/python.asp)*
*The chilkat module is only required if using any source/destination module requiring FTP over SSL or SSH (currently commonapp and fireworks)


INSTALLATION:
To install download and unzip in any directory.


CONFIGURATION:
The script has a set of default settings that you can see in data/config.py.  If you want to make changes you can create a settings.py file put in anything you want to override (using the format setting = value).  You will need to set some things for the script to work (like the authentication information for any source or destination you are using), and unless you're in Hawaii, you almost certainly want to override the GMT offset using the timezone setting.


USAGE:
usage: execute.py [-h] -s SOURCE -d DESTINATION [-t DATE]

Required arguments:
-s SOURCE, --source SOURCE
the source for the file (carnegie, act, sat, commonapp)

-d DESTINATION, --destination DESTINATION
the destination for the file (fireworks)

Optional arguments:
-h, --help
show the help message and exits
  
-t DATESTRING, --date DATESTRING
override the default date behavior of now with a specific date. The date format will depend on the source.
(all current sources use YYYY-MM-DD)


WRITING NEW MODULES:
You can write new source or destination modules and place them in the appropriate subdirectory.  You may name them whatever you like, and the name of the file (minus the .py) becomes what you put in for the SOURCE or DESTINATION on the command line.  Modules must be of class Source or Destination with the following public functions:



class Source:
    def __init__( self, dataroot, config, override_date ):
        self.DATAROOT = dataroot            #path to the data folder for the script
        self.CONFIG = config                #configuration for the script - use self.CONFIG.Get( 'key' )
        self.OVERRIDE_DATE = override_date  #command line date in case you need to override your default date range
        # whatever else you want to do
    
    
    def Retrieve( self ):
        loglines = []   #any information you want logged by the main script, add to the list using loglines.append( 'comment' )
        return <list of file names or False if nothing retrieved>, loglines



class Destination:
    def __init__( self, dataroot, config, source ):
        self.DATAROOT = dataroot    #path to the data folder for the script
        self.CONFIG = config        #configuration for the script - use self.CONFIG.Get( 'key' )
        self.SOURCE = source        #source of the files (in case you have to do a source specific transformation)
        # whatever else you want to do


    def Send( self, files ):
        loglines = []  #any information you want logged by the main script, add to the list using loglines.append( 'comment' )
        return <boolean result of transfer>, loglines


    def Transform( self, files ):
        #used if anything has to be done to the files before they are sent to the destination
        loglines = [] #any information you want logged by the main script, add to the list using loglines.append( 'comment' )
        return <list of file names or False if there were issues>, loglines


