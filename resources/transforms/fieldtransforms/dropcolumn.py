def Transform( oldfield, settings, debug ):
    loglines = []
    if debug:
        loglines.append( 'dropping column with data ' + oldfield )
    return None, loglines
