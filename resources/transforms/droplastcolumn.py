import csv

class Transform:
    def __init__( self ):
        pass


    def Run( self, orgfile, destfile, config ):
        with open( orgfile, "r" ) as source:
            data = csv.reader( source )
            with open( destfile, "w" ) as result:
                if config.get( 'quoteall', True ):
                    wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
                else:
                    wtr = csv.writer( result )
                for row in data:
                    del row[-1]
                    wtr.writerow( row )
        return destfile, ['droplastcolumn transform complete']
