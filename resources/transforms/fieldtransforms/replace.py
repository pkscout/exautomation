import re

def Transform( oldfield, settings, debug ):
    loglines = []
    search = settings.get( 'search', '' )
    replace = settings.get( 'replace', '' )
    default = settings.get( 'default', '' )
    if oldfield:
        newfield = re.sub( search, replace, oldfield )
    else:
        newfield = default
    if not newfield:
        newfield = oldfield
    if debug:
        loglines.append( 'transformed "%s" to "%s" using search of "%s" and replace of "%s" with default of "%s"' % (oldfield, newfield, search, replace, default ) )
    return newfield, loglines
