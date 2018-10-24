import csv
from ..common.fix_utf8 import smartUTF8

class Transform:
    def Run( self, orgfile, destfile, settings ):
        loglines = []
        success = True
        column = settings.get( 'column', -1 ) - 1
        if column < -1:
            return False, ['no column number specified for transform, aborting']
        encoding = settings.get( 'encoding' )
        priority_list = settings.get( 'priority' )
        if encoding:
            source = open( orgfile, "r", encoding=encoding )
        else:
            source = open( orgfile, "r" )
        data = csv.reader( source )
        with open( destfile, "w" ) as result:
            if settings.get( 'quoteall', True ):
                wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
            else:
                wtr = csv.writer( result )
            try:
                for row in data:
                    try:
                        choicelist = row[column]
                    except IndexError as e:
                        loglines.append( 'invalid column number, aborting' )
                        break
                    if priority_list:
                        for priority in priority_list:
                            if priority in choicelist:
                                row[column] = priority
                                break
                    else:
                        row[column] = row[column].split( settings.get( 'delimiter', ',' ) )[0].strip()
                    wtr.writerow( row )
            except UnicodeDecodeError:
                pass
        source.close()
        loglines.append( 'trimchoicelist transform complete' )
        return destfile, loglines
