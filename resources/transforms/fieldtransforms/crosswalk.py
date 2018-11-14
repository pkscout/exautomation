def Transform( oldfield, settings, debug ):
    loglines = []
    crosswalk = settings.get( 'crosswalk', {} )
    if not crosswalk:
        if debug:
            loglines.append( 'no crosswalk provided, returning original field' )
        return oldfield, loglines
    default = settings.get( 'default', oldfield )
    newfield = crosswalk.get( oldfield, default )
    if debug:
        loglines.extend( ['changed %s to %s using crosswalk map:' % (oldfield, newfield ), crosswalk] )
    return newfield, loglines
