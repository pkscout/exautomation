def Transform( oldfield, settings, debug ):
    loglines = []
    if not oldfield:
        return ['', ''], loglines
    if oldfield.startswith( '-' ):
        if debug:
            loglines.append( 'field starts with a dash, so it must be an ACT ID' )        
        return ['', oldfield[1:]], loglines
    if oldfield.startswith( tuple('0123456789') ):
        if debug:
            loglines.append( 'field starts with a number, so it must be a SSN' )        
        return [oldfield, ''], loglines
    if debug:
        loglines.append( 'field is does not seem to be empty, a SSN, or an ACT ID, so it must be the header row' )
    return ['SSN', 'ACT ID'], loglines
