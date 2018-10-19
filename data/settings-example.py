# REQUIRED - IF YOU DELETE THESE EVERYTHING BREAKS
sources = []
destinations = []

# GENERAL CONFIGURATION
# see the default section in config.py for other things you can override here
chilkat_license = 'Anything for 30-day trial' #put license key here after purchase
gmtoffset = '' #put in your GMT offset here, otherwise all times will be GMT

# sources and destinations are construction with modules in the resources/connections directory
# you set the connection module in the type field
# sources and destinations must have a unique name, and source names are used as the directory
# name for destinations that need a directory (like sftp and ftps)
# destinations can filter a file list returned by a source and also transform a file if needed
# filters are just text that must be in the file name
# transforms are modules in the resources/transforms directory
# you set filters for a given source by using <source>:<text>, <source2>:<text2>
# you set transform modules for a given source by using <source>:<module>, <source2>:<module>

# you can delete any of the sources and destinations below if you aren't using them

# CARNEGIE/DARLET SOURCE CONFIGURATION
sources.append( { 'name': 'Carnegie',
                  'type': 'carnegie',
                  'user': '',
                  'auth': ''
                } )

# COMMONAPP SOURCE CONFIGURATION
sources.append( { 'name': 'CommonApp',
                  'type': 'sftp',
                  'user': '',
                  'auth': '',
                  'host': 'ftp.commonapp.org',
                  'dateformat': '%m_%d_%Y'
                } )

# SAT SOURCE CONFIGURATION
sources.append( { 'name': 'SAT',
                  'type': 'sat',
                  'user': '',
                  'auth': ''
                } )

# ACT SOURCE CONFIGURATION


# FIREWORKS DESTINATION CONFIGURATION
destinations.append( { 'name': 'Fireworks',
                       'type': 'ftps',
                       'user': '',
                       'auth': '',
                       'host': 'ftp.gotoextinguisher.com',
                       'port': 997,
                       'passive': True,
                       'authtls': False,
                       'ssl': True,
                       'filters': 'SAT:.csv, CommonApp:.csv',
                       'transforms': 'Carnegie:droplastcolumn, ACT:acttolist',
                     } )
