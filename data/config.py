defaults = { 'chilkat_license': 'Anything for 30-day trial',
             'aborttime': 300,
             'logbackups': 7,
             'gmtoffset': '',
             'override_dateformat': '%Y-%m-%d',
             'dateformat': '%Y-%m-%d',
             'download_max': 0,
             'debug': False,
             'carnegie_baseURL': 'https://my.carnegiecomm.com',
             'carnegie_path': '/client/login/',
             'sat_baseURL': 'https://scoresdownload.collegeboard.org',
             'sat_list_path': '/pascoredwnld/files/list',
             'sat_file_path': '/pascoredwnld/file',
             'sat_dateformat': '%Y-%m-%dT00:00:00',
           }

try:
    import data.settings as overrides
    has_overrides = True
except ImportError:
    has_overrides = False


def Reload():
    if has_overrides:
        reload( overrides )


def Get( name ):
    setting = None
    if has_overrides:
        setting = getattr(overrides, name, None)
    if not setting:
        setting = defaults.get( name, None )
    return setting
    