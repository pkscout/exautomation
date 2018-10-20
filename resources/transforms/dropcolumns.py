import csv

class Transform:
    def __init__( self ):
        pass


    def Run( self, orgfile, destfile, config ):
        columns = config.get( 'columns' )
        if not columns:
            return False, ['no column list provided for dropcolumns transform']
        positives = all(i >= 0 for i in columns)
        negatives = all(i < 0 for i in columns)
        if not ( positives or negatives):
            return False, ['column list for dropcolumns must be all positive or all negative numbers']
        columns.sort( reverse = True )
        with open( orgfile, "r" ) as source:
            data = csv.reader( source )
            with open( destfile, "w" ) as result:
                if config.get( 'quoteall', True ):
                    wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
                else:
                    wtr = csv.writer( result )
                for row in data:
                    for column in columns:
                        del row[column]
                    wtr.writerow( row )
        return destfile, ['dropcolumns transform complete']
