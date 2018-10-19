import csv

class Transform:
    def __init__( self ):
        pass


    def Run( self, orgfile, destfile ):
        with open( orgfile, "r" ) as source:
            data = csv.reader( source )
            with open( destfile, "w" ) as result:
                wtr = csv.writer( result )
                for row in data:
                    del row[-1]
                    wtr.writerow( row )
        return True, []
