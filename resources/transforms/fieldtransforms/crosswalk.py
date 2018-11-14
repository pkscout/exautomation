def Transform( oldfield, settings, debug ):
    loglines = []
    crosswalk = settings.get( 'crosswalk', {} )
    if not crosswalk:
        if debug:
            loglines.append( 'no crosswalk provided, returning original field' )
        return oldfield, loglines
    newfield = crosswalk.get( oldfield, oldfield )
    if debug:
        loglines.extend( ['changed %s to %s using crosswalk map:' % (oldfield, newfield ), crosswalk] )
    return newfield, loglines
