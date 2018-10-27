def Transform( oldfield, transform, debug ):
    loglines = []
    if debug:
        loglines.append['dropping column with data ' + oldfield]
    return False, loglines
