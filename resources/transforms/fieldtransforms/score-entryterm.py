from datetime import datetime, date, timedelta

def Transform( oldfield, settings, debug ):
    loglines = []
    default_term = settings.get( 'default_term', 'Unknown' )
    if not oldfield:
        return default_term, loglines
    scoretype = settings.get( 'scoretype', '' )
    if scoretype.lower() == 'sat':
        fieldparts = oldfield.split( '-' )
        if len( fieldparts ) != 2:
            if debug:
                loglines.append( 'graduation date in unknown format, returning original field' )
            return oldfield, loglines
        gradyear = int( fieldparts[0] )
        gradmonth = int( fieldparts[1] )
    elif scoretype.lower() == 'act':
        try:
            gradyear = int( oldfield )
        except ValueError:
            if debug:
                loglines.append( 'data in field cannot be converted to integer, returning original field' )
            return oldfield, loglines
        gradmonth = 5
    else:
        if debug:
            loglines.append( 'no valid score type provided, returning original field' )
        return oldfield, loglines
    entrytermformat = settings.get( 'entrytermformat', 'Fall %Y' )
    breakmonth = settings.get( 'breakmonth', 8)
    thisyear = datetime.now().year
    thismonth = datetime.now().month
    entry_year = False
    if (gradyear >= (thisyear + 1)) and (gradmonth <= breakmonth):
        entry_year = datetime( year=gradyear, month=gradmonth, day=1 )
    elif (gradyear >= (thisyear + 1)) and (gradmonth > breakmonth):
        entry_year = datetime( year=gradyear+1, month=gradmonth, day=1 )
    elif (gradyear == thisyear) and (thismonth <= breakmonth) and (gradmonth <= breakmonth):
        entry_year = datetime( year=gradyear, month=gradmonth, day=1 )
    elif (gradyear == thisyear) and (thismonth >= breakmonth) and (gradmonth > breakmonth):
        entry_year = datetime( year=gradyear+1, month=gradmonth, day=1 )
    elif (gradyear == (thisyear - 1)) and (thismonth <= breakmonth) and (gradmonth > breakmonth):
        entry_year = datetime( year=thisyear, month=gradmonth, day=1 )
    if entry_year:
        newfield = entry_year.strftime( entrytermformat )
    else:
        newfield = default_term
    if debug:
        loglines.append( 'using grad date of %s returning entry term of %s' % (oldfield, newfield) )
    return newfield, loglines
