defaults = { 'aborttime': 300,
             'logbackups': 5,
             'timezone': '-1000',
             'chilkat_license': 'Anything for 30-day trial',
             'debug': False,
             'carnegie_user': '',
             'carnegie_auth': '',
             'carnegie_baseURL': 'https://my.carnegiecomm.com',
             'carnegie_path': '/client/login/',
             'carnegie_fireworks_path': 'Carnegie/',
             'commonapp_user': '',
             'commonapp_auth': '',
             'commonapp_key': 'commonapp_keyfile',
             'commonapp_key_auth': '',
             'commonapp_baseURL': 'ftps.commonapp.org',
             'commonapp_port': 22,
             'commonapp_timeout': 15000,
             'commonapp_path': '.',
             'commonapp_dateformat': '%Y-%m-%d',
             'commonapp_fireworks_path': 'CommonApp/',
             'sat_user': '',
             'sat_auth': '',
             'sat_baseURL': 'https://scoresdownload.collegeboard.org',
             'sat_list_path': '/pascoredwnld/files/list',
             'sat_file_path': '/pascoredwnld/file',
             'sat_fireworks_path': 'SAT/',
             'fireworks_user': '',
             'fireworks_auth': '',
             'fireworks_baseURL': 'ftp.gotoextinguisher.com',
             'fireworks_port': 997 }

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
    