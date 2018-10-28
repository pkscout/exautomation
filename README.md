# exautomation
Python command line tool to automate various file exchanges

## PREREQUISITES:
* Python 3.x (tested with Python 3.7).  This almost certainly won't work with Python 2.7 (or earlier).  Please see <https://legacy.python.org/dev/peps/pep-0373/> for information on the sunset date for Python 2.7.
* requests module (pip3 install requests)
* pysmb module (pip3 install pysmb)
* chilkat module (download/purchase from http://www.chilkatsoft.com/python.asp)

## INSTALLATION:
To install download and unzip in any directory.

## DIRECTORY STRUCTURE:
### data
All configuration data is stored here.  When upgrading the only files in this directory that should be replaced are `__init__.py` (which is an empty file) and `settings-example.py`.  After the script is run once, it will add three other directories here:  `downloads` (for all downloaded files), `keys` (for any private keys you might need plus host keys saved when connecting via SFTP), and `logs` (for logfiles).

### resources
All shared libraries are stored here.  Unless you are building new modules, you should ever need to be in this directory, but if you do write new modules, they go in either connections or transforms.

## CONFIGURATION:
Copy `settings-example.py` to `settings.py`.  You **MUST** do this, as settings are stored in python dictionaries, so the format of the settings file is important.  There are four sections to the settings:

### Required
The information is this section must exist exactly as it is in `settings-example.py`.  If you change anything in this section the script will almost certainly break.

### General
  The script has a set of default settings that you can override in the settings file (using the format `<setting> = <value>`).This is the section where you can override any of those options.

* `chilkat_license = '<string>'`  
The sftp and ftps connection modules (more on modules in the **MODULES** section below) require a separately purchased and licensed module to work (see **PREREQUISITES** above).  Once you purchase the license you need to add the license key to the settings file.  If you don't enter a key, the script will activate a free 30 day trial the first time you run it.

* `download_max = <integer>`  
By default all downloaded and converted files are saved. To cap the size of the download directory, add this to set a max size for the download directory (in megabytes).

* `override_dateformat = '<string>'`  
When calling the script you can override the default date behavior (see **USAGE** below for more details).  This is the format expected when using that option.  The default is `%Y-%m-%d` (yyyy-mm-dd) but you can use any valid date format string you like to override this.

* `dateformat = '<string>'`  
All modules by default filter files to retrieve based on date, and this is the default date format if you don't put anything in your source configuration.  You can change the default behavior of `%Y-%m-%d` (yyyy-mm-dd) by adding this to the settings.

* `aborttime = <integer>`  
The time in seconds the script will wait for another instance of itself to finish before aborting.

* `logbackups = <integer>`  
By default the logs are rolled every day and seven days of logs are kept.  You can change the number of days of logs kept with this setting.

* `debug = <boolean>`  
If you're having problems, you can enable debug logging by adding `debug = True` to the settings.  This generates **lots** of information, so it isn't recommended to leave debugging enabled.  **Please note that certain connection modules will log the usernames and password in plaintext.  Also, while in debug mode some modules may log PII for prospective students, so please be aware of that and understand your obligations under local, state, and federal laws/regulations as well as your institutional policies.  If you're going to share the logs for some reason make sure you scrub them first.**

### Sources
This is the section where you define from where you'll be getting files.  Source configurations are stored as python dictionaries, so the format is important.  You are encouraged to use `settings-example.py` as a template for any new sources you add.  Sources must at a minimum have a name (all source names must be unique and may contain only letters, numbers, and a few special characters like dash and underscore) and a type (more on the types in the **MODULES** section below) as well as some configuration options based on the type.  

By default sources get yesterday's files based on either the default date format or one specific to the source (defined by adding `'dateformat':'<string>'` to the source configuration).  You can include a different filter if you want in the source configuration using `'filter':'<string>'` where string is either plain text or a regular expression.  The date (or filter) can be overridden from the command line if needed (see **USAGE** section for more details).

### Destinations
This is the section where you define where you'll be sending files after they are downloaded.  Destination configurations are stored as python dictionaries, so the format is important.  You are encouraged to use `settings-example.py` as a template for any new destinations you add.  Destinations must at a minimum have a name (all destination names must be unique and may contain only letters, numbers, and a few special characters like dash and underscore) and a type (more on the types in the **MODULES** section below) as well as some configuration options based on the type.  

Destinations can filter a file list returned by a source.  You set filters for a given source by using `'filters':'<source>: <string>, <source2>: <string>'`.  Filters can be plain text or regular expressions.  If a filename includes the plain text or matches the regular expression, then it will be passed on for further proccessing.  

Destinations can also tranform files before sending (see **MODULES** below for a list of available transforms).  You set transform modules for a given source by using `'transforms': '<source>: <module>, <source2>: <module2>'`.  Transforms can be chained together by using `<source>: <module>; <module2>; <module3>` (note the semi-colon for separating transform modules).  Tranforms will happen in the order listed.  Transforms can have configurations (based on the transform).  To configure a transform add `'<source>_<transform>_config': <config_dict>` where `<config_dict>` is a python dict (see `settings-example.py` for examples).  Note that the ACT transform in the Fireworks destination in `settings-example.py` actually converts the ACT fixed width to a CSV for Fireworks so you might want to keep that to use somewhere.  

By default any destination that places files (currently they all do) will place files in a subdirectory matching the name of the source.  This is to ensure that duplicate files names across sources don't cause an issue.  You can override this by putting `'sourcefolders': '<source1>: <path>, <source2>: <path2>'` in the configuration dictionary for the destination.  The path will be relative to the path you set for the destination and must be appropriate for the destination (e.g. if it's a sftp source you would use `this/is/the/path`).  If a given source doesn't have an override path then the default sourcefolder path will be used.  If you put all files from all sources in the same directory you are on your own to deal with duplicate file names.  **This script will overwrite existing files with the same names as names it's planning to use.  You have been warned.**

## Modules
There are three types of modules: connection modules, transform modules, and field transform modules (which are used by the changefields module).  Many connection modules require authentication of some sort, and those are stored as plain text in settings.py as needed.  Yes, putting usernames and passwords in a text file is not secure, but since the script needs to read them unattended, there is technically no way to completely secure the passwords if someone has access to the machine on which this is running.  Future versions may address this, but please don't hold your breath waiting.

### Connection Modules

#### Secure FTP (sftp)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login - can be omitted if using a private key)  
`'host': '<string>'` (domain name of server)

* **Optional Settings**  
`'path':'<string>'` (path to the directory where the files are, defaults to the root directory)  
`'port': <integer>` (sftp port, defaults to 22)  
`'key_auth': '<string>'` (if using an encrypted private key, the passphrase to decrypt it)  
`'timeout': <integer>` (time before connection attempt aborts in milliseconds, defaults to 15000)

* **Notes**  
If you want to use a private key, it needs to go in the data/keys folder named as `<sourcename>_private.key` (this is case senstive, so if sourcename has capital letters, the file name needs them too).  
During the first connection to a SFTP server, the script will save the hostkey provided by the server in `data/keys` with a name in the format `<sourcename>_host.key`.  If the host provides a different key later, SFTP will not connect.  If this happens, you should confirm that the server has really moved and delete the host key to generate a new one.

#### FTP over SSL (ftps)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login)  
`'host': '<string>'` (domain name of server)

* **Optional Settings**  
`'path': '<string>'` (path to the directory where the files are, defaults to the root directory)  
`'port': <integer>` (ftps port, defaults to 990)  
`'timeout': <integer>` (time before connection attempt aborts in milliseconds, defaults to 15000)  
`'authtls': <boolean>` (whether to use authtls to secure connection, default `True`)  
`'ssl': <boolean>` (whether to use ssl to secure connection, default `False`)  
`'passive': <boolean>` (whether to use passive mode, default `False`)

* **Notes**  
The authtls and ssl settings are mutually exclusive.  If you set both to `True`, authtls will be used.  
You can technically use this module for an unsecured FTP connection by setting both authtls and ssl to `False` and setting the appropriate port.  Please don't do this unless it's a local connection that is secured some other way.

#### Local File (localfile)
* **Required Settings**  
`'path': '<string>'` (path to the directory where the files are)  

* **Notes**  
The directory path needs to be noted in POSIX format (i.e. `/this/is/the/path`) and start at the root directory for the file system.  For Windows include the drive letter as the first directory (i.e. `/C:/this/is/the/path`).
You should be able to use this to access any file on any mounted drive (even if that mounted drive is a network share, although on Windows it will need to mapped to a drive letter).

#### Windows Share (smb)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login)  
`'host': '<string>'` (Windows name of the server)  
`'hostip': '<string>'` (IP address of the server)  
`'clientname': '<string>'` (name of local client - can be basically anything under 16 characters)  
`'share': '<string>'` (the name of the share to which you will connect)

* **Optional Settings**  
`'port': <integer>` (port of the server, default `445`)  
`'domainname': '<string>'` (the name of the domain to which the server belongs)  
`'usentlmv2': <boolean>` (whether or not to use NTLM v2, default `True`)  
`'isdirectip': <boolean>` (whether to use Direct Hosting over TCP or NetBIOS, default `True`)  

* **Notes**  
The directory path needs to be noted in POSIX format (i.e. `this/is/the/path`) and references the path on the share to which you will be connecting.  Note that you **SHOULD NOT** include a forward slash at the beginning.

#### SAT Score Retreiver (sat)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login)  
`'dateformat': '%Y-%m-%dT00:00:00-<UTCOFFSET>'`  

* **Notes**  
This connection module uses the College Board API to retrieve files.  The remaining connection information is in `config.py`.  You can technically override those configs by adding the items from `config.py` to `settings.py`, but if any of those change the module will likely have to be updated anyway, as it means something major changed.  
SAT has a very special required date format.  UTCOFFSET is your hours from Greenwich Mean Time.  For instance this would be -0500 for the eastern time zone of the US.

#### Carnegie/Darlet Prospect Retreiver (carnegie)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login)  

* **Notes**  
This connection module simulates a login to the Carnegie/Darlet member web site and then screen scrapes to get the file.  The remaining connection information is in `config.py`.  You can technically override those configs by adding the items from `config.py` to `settings.py`, but if any of those change the module will likely have to be updated anyway, as it means something major changed.

### Transform Modules 

#### File Rename (filerename)
This module renames a file based on a pair of regular expressions (one for the search and the other the replace.)
* **Required Settings**  
`'search':r'<string>'` (regular expression search like `(.*).txt`)  
`'replace':r'<string>'` (regular expression replace like `\1.csv`)

* **Optional Settings**
`'appendstring': <boolean>` (Defaults to `False`, if set to `True` string below will be appended to end of file name  
`'string': <string>` (if this is omited with appendstring set to `True` it will insert today's date)  
`'dateformat': <string>` (if inserting date, formats the date using any valid date format and defaults to `%Y-%m-%d`)

* **Notes**  
By putting `r` in front of the string for the search and replace sections you don't have to escape slash characters.


#### Fixed Width File to CSV (fixedtocsv)
This module transforms a fixed width file into a CSV file.  The configuration dictionary for this transforms takes three settings:
* **Required Settings**  
`'colspec': <list of tuples>`  
example: `'colspec': [(1,5), (6,22), (23,23)]` (this would break the file into three CSV columns with data from characters 1 - 3, 6 - 22, and the single character at 23)

* **Optional Settings**  
`'header': <list of strings>` (if no header is included, it's assumed don't need one for your destination)  
example: `'header': ['First Name', 'Last Name', 'Opt Out']`  
`'encoding': '<string>'` (Defaults to Python discovery method.  Other options are listed at <https://docs.python.org/3.7/library/codecs.html#standard-encodings>)

#### Transform Fields (changefields)
This module has a bunch of sub modules (described below) that allow you to do various things to a field of data (like do a regular expression search and replace, trim a pick list to one entry, and even drop entire columns).  The configuration for this transform is a bit tricky, so definitely look at the example in settings-example.py for some guidance.

* **Required Settings**  
`'transforms': <list of dictionaries>` (see **FIELD TRANFORMS** below for details on dictionaries for specific field transforms)

* **Optional Settings**  
`'quoteall': <boolean>` (Defaults to `True` and ensures all data is quoted in the saved CSV.  Set to `False` to remove all quoting)  
`'encoding': '<string>'` (Defaults to Python discovery method.  Other options are listed at <https://docs.python.org/3.7/library/codecs.html#standard-encodings>)

* **Notes**  
You can use a field transform more than once in a row simply by adding another item to the list with the appropriate column reference.  Field transforms are all done on CSV files.  You must convert your file to CSV before using this transform.

### Field Transform Modules

#### Drop Column (dropcolumn)
This module drops the given column from the file completely.

* **Required Settings**  
`'column': <integer>` (the column to be dropped - first column is column 0)  
`'name': 'dropcolumn'`

#### Replace Text (replace)
This module does a search based on a regular expression then the corresponding replace with another regular expression.

* **Required Setting**  
`'column': <integer>` (the column where the text lives - first column is column 0)  
`'name': 'replace'`  
`'search': r'<regular expression>'` (the regular expression that will define the search criteria)  
`'replace': r'<regular expression>'` (the regular expression that defines the replace)

* **Optional Settings**  
`'default': '<string>'` (If the field is empty, put this default value in the field instead)

* **Notes**  
If your `search` doesn't find anything, the entire original field will be returned.  
By putting `r` in front of the string for the search and replace sections you don't have to escape slash characters.

#### Trim Choice List (trimchoicelist)
This module allows you to take a choice list field  (i.e. a list of things separated by a delimiter) and keep only one of them (either the first one or based on a priority list).  This is useful if one of your sources has a question that allows multiple answers to a question but your destination only allows one answer.

* **Required Settings**  
`'column': <integer>` (the column where the choice list answers lives - first column is column 0)  
`'name': 'trimchoicelist'`

* **Optional Settings**  
`'priority':<list of strings>` (all the possible choices listed in the order you want them considered)  

* **Notes**  
If you don't include a priority list, the first choice in the list is taken and the rest are ignored.  If no item in a choice list matches any of the priorities, the entire original field is maintained for that field.

## USAGE:
`usage: execute.py [-h] -s SOURCE -d DESTINATION [-f STRING]`

### Required arguments:
`-s SOURCE, --source SOURCE`  
the source for the file

`-d DESTINATIONS, --destination DESTINATIONS`  
the destinations for any files retrieved by the source (multiple destinations should be separated by a colon)

### Optional arguments:
`-f STRING, --filter STRING`  
Overrides the default date behavior or source filter.

`-h, --help`  
show the help message and exits

## SCHEDULING TASKS:
Obviously an automation tool isn't much use if you can't schedule it.  How you do that is going to be a bit dependent on platform, but generally you will need to call your Python interpreter and then provide the full path to execute.py with valid command line options.  Note that since the script can only do one source at a time, you'll need to schedule different jobs for each different source (or write your own wrapper script to loop through them if you want to).  On Windows you're probably going to use Task Scheduler, and after creating a new task to run daily at a certain time, that might look like:

Program/script: `"C:\Program Files\Python 3.7\pythonw.exe"`  
Add arguments: `"C:\CustomApps\exautomation\execute.py -s SAT -d Fireworks"`  
Start in: `"C:\CustomApps\exautomation\"`

On most Unix variants, you'll use crontab.  The line you add to your crontab might look like:

`15 05 * * * /usr/bin/python3 /home/automation/Scripts/exautomation/execute.py -s sat -f fireworks  > /dev/null 2>&1`


## WRITING NEW MODULES:

You can write new connection, transform, and field transform modules and place them in the appropriate subdirectory of the resources directory (note: field transforms go in transforms/field transforms).  You may name them whatever you like, and the name of the file (minus the .py) becomes what you put use in the settings file and command line.  Connection modules must have one public class called Connection with the following public functions:

```python
from ..common.remotesites import parseSettings

class Connection:
    def __init__( self, config, settings ):
        defaults = parseSettings( config, settings )        
        self.LOCALDOWNLOADPATH = defaults.get( 'localdownloadpath' )
        self.REMOTEFILTER = defaults.get( 'remotefilter' )
        self.SOURCEFOLDER = defaults.get( 'sourcefolder' )
        # LOCALDOWNLOADPATH is the data/downloads directory (source for Upload and destination for Download)
        # REMOTEFILTER is a string (either date, text or regular expression) you can use to filter your list of files in download
        # SOURCEFOLDER is the name of the destination subdirectory for Upload
        # access all the options set in the source or destination section by using settings.get( 'name of setting' )
        # access configuration items using config.Get( 'name of config item' )
        # note that config is NOT a dictionary and has a special function called Get (capital G)


    def Download( self ):
        # whatever you're going to do to download files
        return <list of files>, <list of log lines you'd like to add to the log>


    def Upload( self, files ):
        # whatever you're going to do to upload files
        return <boolean indicating file outcome of upload>, <list of log lines you'd like to add to the log>
```

Transform modules must have one public class named Transform with the following public functions:

```python
class Transform:
    def Run( self, orgfile, destfile, settings, debug ):
        # whatever you're going to do to transform the file
        # orgfile and destfile are full file paths and should not be changed
        # debug is True if debugging is set in settings, so this lets you return more detailed loglines if you wish
        return destfile, <list of log lines you want to add to the log>
```

Field Transform modules must have one public function as follows:

```python
def Transform( oldfield, transform, debug ):
    # whatever you're going to do to transform the field
    # all settings for the tranform can be referenced using transform.get( 'name' )
    # debug is True if debugging is set in settings, so this lets you return more detailed loglines if you wish
    return <string that is the transformed field>, <list of log lines you want to add to the log>
```

If you would like to submit your modules to the github repo as a pull request, I can add review and add them so others can use them too.  If you decide to do that, please provide an appropriate license that is compatible with the license under which this code is released.
