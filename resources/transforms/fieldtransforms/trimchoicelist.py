def Transform( oldfield, settings, debug ):
    loglines = []
    priority_list = settings.get( 'priority', [] )
    newfield = oldfield
    for priority in priority_list:
        if priority in oldfield:
            newfield = priority
            break
    if newfield == oldfield:
        newfield = oldfield.split( settings.get( 'delimiter', ',' ) )[0].strip()
    if debug:
        loglines.extend( ['the priority list is:', priority_list] )
        loglines.append( 'selected "%s" from "%s"' % (newfield, oldfield) )
    return newfield, loglines
