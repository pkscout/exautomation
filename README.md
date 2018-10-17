# exautomation
Python command line tool to automate various file exchanges

**PREREQUISITES:**
* Python 3.x (tested with Python 3.7, might work with Python 2.x, but I doubt it)
requests module (pip3 install requests)
* chilkat module (download/purchase from http://www.chilkatsoft.com/python.asp)


**INSTALLATION:**
To install download and unzip in any directory.


**DIRECTORY STRUCTURE:**
*data*
All configuration data is stored here.  When upgrading the only files in this directory that should be replaced are __init__.py, config.py and settings-example.py.  After the script is run once, it will add three other directories here:  downloads (for all downloaded files), keys (for any private keys you might need plus host keys saved when connecting via SFTP), and logs (for logfiles).

*resources*
All shared libraries are stored here.  Unless you are building new modules, you should ever need to be in this directory, but if you do write new modules, they go in either sources or destinations.


**CONFIGURATION:**
The script has a set of default settings that you can see in data/config.py.  If you want to make changes you can create a settings.py file put in anything you want to override (using the format setting = value) or copy the settings-example.py to settings.py and update as needed.

* The commonapp and fireworks modules require a separately purchased licensed module to work (see PREREQUISITES).  Once you purchase it you need to add chilkat_license = <string> to the settings.py file where <string> is the license key.  If you don't enter a key, the script will activate a free 30 day trial the first time you run it.

* all modules require authentication of some sort, so remember to fill out those sections in settings.py as needed.  You can leave the authentication blank for a given module if you are not using that module.

* By default all downloaded and converted files are saved. To cap the size of the download directory, add download_max = x to the settings.py file where x is megabytes.

* By default logs are rolled every day and saved for seven days.  To keep a different number of log files add logbackup = x to the settings.py file where x is number of days.

* By default the log stores a minimal amount of information.  If you're having problems, you can enable debug logging by adding debug = True to the settings.py file.  This generates *lots* of information, so it isn't recommended to leave debugging enabled.

* If you are using a module that is connecting via SFTP or SSH, the module supports using a public/private key pair for authentication.  You must place the appropriate key in the keys directory with the name <module>-private.key where <module> is the name of the module file (minus .py).  You are on your own as how to generate the appropriate key pairs and get the key to the particular source in the right place.  Currently only the commonapp module using SFTP.

* If you are using an encrypted key for public/private key pair authentication, you need to add <module>_key_auth = <password> to settings.py where <module> is the name of the module file (minus .py) and <password> is the password for the key.


**USAGE:**
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


**SCHEDULING TASKS:**
Obviously an automation tool isn't much use if you can't schedule it.  How you do that is going to be a bit dependent on platform, but generally you will need to call your Python interpreter and then provide the full path to execute.py with valid command line options.  Note that since the script can only do one pair of SOURCE/DESTINATION at a time, you'll need to schedule different jobs for each different pair (or write your own wrapper script to loop through them if you want to).  On Windows you're probably going to use Task Scheduler, and after creating a new task to run daily at a certain time, that might look like:

    Program/script: "C:\Program Files\Python 3.7\pythonw.exe"
    Add arguments: "C:\CustomApps\exautomation\execute.py -s sat -d fireworks"

On most Unix variants, you'll use crontab.  The line you add to your crontab might look like:

    15 05 * * * /usr/bin/python3 /home/automation/Scripts/exautomation/execute.py -s sat -f fireworks  > /dev/null 2>&1


**WRITING NEW MODULES:**
You can write new source or destination modules and place them in the appropriate subdirectory.  You may name them whatever you like, and the name of the file (minus the .py) becomes what you put in for the SOURCE or DESTINATION on the command line.  You will likely need to add some configuration options, and those should be added to data/config.py in the default section (and can be overriden in settings.py).  The general naming convention for config settings is modulename_configname.  Modules must be of class Source or Destination with the following public functions:


```python
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
        self.CONFIG = config        #configuration for the script - use self.CONFIG.Get( 'key' ) to retrieve a given config option
        self.SOURCE = source        #source of the files (in case you have to do a source specific transformation)
        # whatever else you want to do


    def Send( self, files ):
        loglines = []  #any information you want logged by the main script, add to the list using loglines.append( 'comment' )
        return <boolean result of transfer>, loglines


    def Transform( self, files ):
        #used if anything has to be done to the files before they are sent to the destination
        loglines = [] #any information you want logged by the main script, add to the list using loglines.append( 'comment' )
        return <list of file names or False if there were issues>, loglines
```

If you would like to submit your modules to the github repo as a pull request, I can add review and add them so others can use them too.  If you decide to do that, please provide an appropriate license that is compatible with the license under which this code is released.
