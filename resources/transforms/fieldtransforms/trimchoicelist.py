def Transform( oldfield, transform, debug ):
    loglines = []
    priority_list = transform.get( 'priority', [] )
    newfield = oldfield
    for priority in priority_list:
        if priority in oldfield:
            newfield = priority
            break
    if newfield == oldfield:
        newfield = oldfield.split( transform.get( 'delimiter', ',' ) )[0].strip()
    if debug:
        loglines.extend( ['the priority list is:', priority_list] )
        loglines.append( 'selected "%s" from "%s"' % (newfield, oldfield) )
    return newfield, loglines
