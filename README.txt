# exautomation
Python command line tool to automate various file exchanges


PREREQUISITES:
Python 3.x (tested with Python 3.7, might work with Python 2.x, but I doubt it)
requests module (pip3 install requests)
chilkat module (download/purchase from http://www.chilkatsoft.com/python.asp)


INSTALLATION:
To install download and unzip in any directory.


CONFIGURATION:
The script has a set of default settings that you can see in data/config.py.  If you want to make changes you can create a settings.py file put in anything you want to override (using the format setting = value) or copy the settings-example.py to settings.py and update as needed.

• The commonapp and fireworks modules require a licensed module to work.  Once you purchase it (see URL above) you need to add chilkat_license = <string> where <string> is the license key to the settings.py file.  The script will activate a free 30 day trial the first time you run it.

• all modules require authentication of some sort, so remember to fill out those sections as needed.  You can leave the authentication blank for a given module if you are not using that module.

• By default all downloaded and converted files are saved. To cap the size of the download directory, add download_max = x (where x is megabytes) to the settings.py file.

• By default logs are rolled every day and saved for seven days.  To keep a different number of log files add logbackup = x (where x is number of days) to the settings.py file.

• By default the log stores a minimal amount of information.  If you're having problems, you can enable debug logging by adding debug = True to the settings.py file.  This generates *lots* of information, so it isn't recommended to leave debugging enabled.


USAGE:
usage: execute.py [-h] -s SOURCE -d DESTINATION [-t DATE]

Required arguments:
-s SOURCE, --source SOURCE
the source for the file

-d DESTINATION, --destination DESTINATION
the destination for the file

Optional arguments:
-h, --help
show the help message and exits
  
-t DATESTRING, --date DATESTRING
By default the script gets yesterday's files.  If you override the default date behavior with a specific date (format yyyy-mm-dd) it will get the files for that date.  You can change the date format for the override date by adding override_dateformat = <string> where <string> is a valid date format.


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


