# v.0.1.0

import chilkat, os
from .fileops import readFile, writeFile
from .hostkeys import CheckHostKey

def ConnectSFTP( config ):
    loglines = []
    key = chilkat.CkSshKey()
    privatekey = key.loadText( config.get( 'privatekeypath' ) )
    if key.get_LastMethodSuccess() == True:
        if config.get( 'key_auth' ):
            key.put_Password( config.get( 'key_auth' ) );
        success = key.FromOpenSshPrivateKey( privatekey )
        if (success != True):
            key = None   
    else:
        key = None
    loglines.append( 'connecting to %s server' % config.get( 'module_name', '' ) )
    sftp = chilkat.CkSFtp()
    success = sftp.UnlockComponent( config.get( 'chilkat_license', 'Anything for 30 day trial' ) )
    if (success != True):
        loglines.append( sftp.lastErrorText() )
        return False, loglines
    sftp.put_ConnectTimeoutMs( config.get( 'timeout', 15000 ) )
    sftp.put_IdleTimeoutMs( config.get( 'timeout', 15000 ) )
    success = sftp.Connect( config.get( 'host' ), config.get( 'port', 22 ) )
    if (success != True):
        loglines.append( sftp.lastErrorText() )
        return False, loglines
    success, cloglines = CheckHostKey( sftp.hostKeyFingerprint(), config.get( 'hostkey' ) )
    if config.get( 'debug' ):
        loglines.extend( cloglines )
    if not success:
        loglines.append( 'WARNING: HOSTKEY FOR %s SERVER DOES NOT MATCH SAVED KEY. ABORTING.' % config.get( 'module_name', '' ).upper() )
        return False, loglines
    if key:
        loglines.append( 'trying to authentication using private key' )
        success = sftp.AuthenticatePk( config.get( 'username', '' ), key )
    else:
        success = False
    if (success != True):
        if key and config.get( 'debug' ):
            loglines.append( sftp.lastErrorText() )
        elif key:
            loglines.append( 'private key based authentication failed' )
        loglines.append( 'trying to authentication with username and password' )
        success = sftp.AuthenticatePw( config.get( 'username', '' ), config.get( 'auth', '' ) )
        if (success != True):
            loglines.append( sftp.lastErrorText() )
            return False, loglines
    success = sftp.InitializeSftp()
    if (success != True):
        loglines.append( sftp.lastErrorText() )
        return False, loglines
    return sftp, loglines


def ConnectFTPS( config ):
    loglines = []
    ftps = chilkat.CkFtp2()
    success = ftps.UnlockComponent( config.get( 'chilkat_license', 'Anything for 30 day trial' ) )
    if (success != True):
        loglines.append( ftps.lastErrorText() )
        return False, loglines
    loglines.append( 'connecting to %s server' % config.get( 'module_name', '' ) )
    ftps.put_Passive( config.get( 'ftps_passive', False ) )
    ftps.put_Hostname( config.get( 'host' ) )
    ftps.put_Username( config.get( 'username' ) )
    ftps.put_Password( config.get( 'auth' ) )
    ftps.put_Port( config.get( 'port', 990 ) )
    ftps.put_AuthTls( config.get( 'ftps_authtls', True ) )
    ftps.put_Ssl( config.get( 'ftps_ssl', False ) )
    success = ftps.Connect()
    if (success != True):
        loglines.append( ftps.lastErrorText() )
        return False, loglines
    return ftps, loglines
