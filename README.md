# exautomation
Python command line tool to automate various file exchanges

## PREREQUISITES:
* Python 3.x (tested with Python 3.7).  This almost certainly won't work with Python 2.7 (or earlier).  Please see <https://legacy.python.org/dev/peps/pep-0373/> for information on the sunset date for Python 2.7.
* requests module (pip3 install requests)
* chilkat module (download/purchase from http://www.chilkatsoft.com/python.asp)


## INSTALLATION:
To install download and unzip in any directory.


## DIRECTORY STRUCTURE:
### data
All configuration data is stored here.  When upgrading the only files in this directory that should be replaced are `__init__.py`, `config.py` and `settings-example.py`.  After the script is run once, it will add three other directories here:  `downloads` (for all downloaded files), `keys` (for any private keys you might need plus host keys saved when connecting via SFTP), and `logs` (for logfiles).

### resources
All shared libraries are stored here.  Unless you are building new modules, you should ever need to be in this directory, but if you do write new modules, they go in either connections or transforms.

## CONFIGURATION:
Copy `settings-example.py` to `settings.py`.  You **MUST** do this, as settings are stored in python dictionaries, so the format of the settings file is important.  There are four sections to the settings:

### Required
The information is this section must exist exactly as it is in `settings-example.py`.  If you change anything in this section the script will almost certainly break.

### General
  The script has a set of default settings that you can override in the settings file (using the format `<setting> = <value>`).This is the section where you can override any of those options.

* `chilkat_license = <string>`  
The sftp and ftps connection modules (more on modules in the **MODULES** section below) require a separately purchased and licensed module to work (see **PREREQUISITES** above).  Once you purchase the license you need to add the license key to the settings file.  If you don't enter a key, the script will activate a free 30 day trial the first time you run it.

* `gmtoffet = <string>`  
Set to your local offset in format -xxxx (i.e. -1000 or +0600).  Right now the SAT module is the only thing that uses this.  If you don't set this all times for the SAT module will be in Greenwich Mean Time.

* `download_max = <integer>`  
By default all downloaded and converted files are saved. To cap the size of the download directory, add this to set a max size for the download directory (in megabytes).

* `override_dateformat = <string>`  
When calling the script you can override the default date behavior (see **USAGE** below for more details).  This is the format expected when using that option.  The default is `%Y-%m-%d` (yyyy-mm-dd) but you can use any valid date format string you like to override this.

* `dateformat = <string>`  
All modules by default filter files to retrieve based on date, and this is the default date format if you don't put anything in your source configuration.  You can change the default behavior of `%Y-%m-%d` (yyyy-mm-dd) by adding this to the settings.

* `aborttime = <integer>`  
The time in seconds the script will wait for another instance of itself to finish before aborting.

* `logbackups = <integer>`  
By default the logs are rolled every day and seven days of logs are kept.  You can change the number of days of logs kept with this setting.

* `debug = <boolean>`  
If you're having problems, you can enable debug logging by adding `debug = True` to the settings.  This generates **lots** of information, so it isn't recommended to leave debugging enabled.  Please also note that certain connection modules will log the usernames and password in plaintext, so if you're going to share the logs for some reason make sure you scrub them first. 

### Sources
This is the section where you define from where you'll be getting files.  Source configurations are stored as python dictionaries, so the format is important.  You are encouraged to use `settings-example.py` as a template for any new sources you add.  Sources must at a minimum have a name (all source names must be unique) and a type (more on the types in the **MODULES** section below) as well as some configuration options based on the type.  

By default sources get yesterday's files based on either the default date format or one specific to the source (defined by adding `'dateformat':'<string>'` to the source configuration).  You can include a different filter if you want in the source configuration using `'filter':'<string>'` where string is either plain text or a regular expression.  The date (or filter) can be overridden from the command line if needed (see **USAGE** section for more details).

### Destinations
This is the section where you define where you'll be sending files after they are downloaded.  Destination configurations are stored as python dictionaries, so the format is important.  You are encouraged to use `settings-example.py` as a template for any new destinations you add.  Destinations must at a minimum have a name (all destination names must be unique) and a type (more on the types in the **MODULES** section below) as well as some configuration options based on the type.  

Destinations can filter a file list returned by a source and also transform a file if needed.  You set filters for a given source by using `'filters':'<source>: <string>, <source2>: <string>'`.  Filters can be plain text or regular expressions.  If a filename includes the plain text or matches the regular expression, then it will be passed on for further proccessing.  

Destinations can also tranform a file before sending (see **MODULES** below for a list of available transforms).  You set transform modules for a given source by using `'transforms': '<source>: <module>, <source2>: <module2>'`.  Transforms can have configurations (based on the transform).  To configure a transform add `'<source>_<transform>_config': <config_dict>` where `<config_dict>` is a python dict (see `settings-example.py` for examples).  Note that the ACT transform in the Fireworks destination in `settings-example.py` actually converts the ACT fixed width to a CSV for Fireworks so you might want to keep that to use somewhere.  

By default any destination that places files (currently they all do) will place files in a subdirectory matching the name of the source.  This is to ensure that duplicate files names across sources don't cause an issue.  You can override this by putting `'sourcefolders': '<source1>: <path>, <source2>: <path2>'` in the configuration dictionary for the destination.  The path will be relative to the path you set for the destination and must be appropriate for the destination (e.g. if it's a sftp source you would use `this/is/the/path`).  If a given source doesn't have an override path then the default sourcefolder path will be used.  If you put all files from all sources in the same directory you are on your own to deal with duplicate file names.  **This script will overwrite existing files with the same names as names it's planning to use.  You have been warned.**

## MODULES
There are two types of modules: connection modules and transform modules.  Many connection modules require authentication of some sort, and those are stored as plain text in settings.py as needed.  Yes, putting usernames and passwords in a text file is not secure, but since the script needs to read them unattended, there is technically no way to completely secure the passwords if someone has access to the machine on which this is running.  Future versions may add password encryption with a passphrase stored in the settings (still not secure, but perhaps it'll make someone feel better).

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
The directory path needs to be noted in proper format for your operating system and start at the root directory for the file system.  For Unix variants (including Mac OSX) That means `/this/is/the/path`.  For Windows you have to use `C:\\this\\is\\the\\path`.
You should be able to use this to access any file on any mounted drive (even if that mounted drive is a network share, although on Windows it will probably need to mapped to a drive letter).

#### SAT Score Retreiver (sat)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login)  

* **Notes**  
This connection module uses the College Board API to retrieve files.  The remaining connection information is in `config.py`.  You can technically override those configs by adding the items from `config.py` to `settings.py`, but if any of those change the module will likely have to be updated anyway, as it means something major changed.

#### Carnegie/Darlet Prospect Retreiver (carnegie)
* **Required Settings**  
`'user': '<string>'` (account used to login)  
`'auth': '<string>'` (password for login)  

* **Notes**  
This connection module simulates a login to the Carnegie/Darlet member web site and then screen scrapes to get the file.  The remaining connection information is in `config.py`.  You can technically override those configs by adding the items from `config.py` to `settings.py`, but if any of those change the module will likely have to be updated anyway, as it means something major changed.

### Transform Modules
**STILL NEED TO WRITE THIS**

## USAGE:
`usage: execute.py [-h] -s SOURCE -d DESTINATION [-f STRING]`

### Required arguments:
`-s SOURCE, --source SOURCE`  
the source for the file

`-d DESTINATIONS, --destination DESTINATIONS`  
the destinations for any files retrieved by the source (multiple destinations should be separated by a colon)

### Optional arguments:
`-h, --help`  
show the help message and exits
  
`-f STRING, --filter STRING`  
Overrides the default date behavior or source filter.

## SCHEDULING TASKS:
Obviously an automation tool isn't much use if you can't schedule it.  How you do that is going to be a bit dependent on platform, but generally you will need to call your Python interpreter and then provide the full path to execute.py with valid command line options.  Note that since the script can only do one source at a time, you'll need to schedule different jobs for each different source (or write your own wrapper script to loop through them if you want to).  On Windows you're probably going to use Task Scheduler, and after creating a new task to run daily at a certain time, that might look like:

`Program/script: "C:\Program Files\Python 3.7\pythonw.exe"
Add arguments: "C:\CustomApps\exautomation\execute.py -s sat -d fireworks"`

On most Unix variants, you'll use crontab.  The line you add to your crontab might look like:

`15 05 * * * /usr/bin/python3 /home/automation/Scripts/exautomation/execute.py -s sat -f fireworks  > /dev/null 2>&1`


## WRITING NEW MODULES:

You can write new connection and transform modules and place them in the appropriate subdirectory.  You may name them whatever you like, and the name of the file (minus the .py) becomes what you put use in the settings file and command line.  The general naming convention for config settings is modulename_configname.  Connection modules must have one public class called Connection with the following public functions:

```python
code samples go here
```

Transform modules must have one public class named Transform with the following public functions:

```python
code samples go here
```

If you would like to submit your modules to the github repo as a pull request, I can add review and add them so others can use them too.  If you decide to do that, please provide an appropriate license that is compatible with the license under which this code is released.
