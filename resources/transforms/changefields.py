import csv, sys
import resources.transforms.fieldtransforms

field_modules = {}
for module in resources.transforms.fieldtransforms.__all__:
    full_plugin = 'resources.transforms.fieldtransforms.' + module
    __import__( full_plugin )
    imp_plugin = sys.modules[ full_plugin ]
    field_modules[module] = imp_plugin

class Transform:
    def Run( self, orgfile, destfile, settings, debug ):
        loglines = []
        if not settings.get( 'transforms' ):
            return False, ['no transforms provided for field transforms']
        columns = settings.get( 'columns' )
        if not columns:
            return False, ['no column list provided for field transforms']
        positives = all( i >= 0 for i in columns )
        negatives = all( i < 0 for i in columns )
        if not ( positives or negatives):
            return False, ['column list for field transforms must be all positive or all negative numbers']
        columns.sort( reverse = True )
        encoding = settings.get( 'encoding' )
        if len( settings.get( 'transforms' ) ) == 1:
            transforms = []
            for column in columns:
                transforms.append( settings.get( 'transforms' )[0] )
        else:
            transforms = settings.get( 'transforms' )
        if encoding:
            source = open( orgfile, "r", newline='', encoding=encoding )
        else:
            source = open( orgfile, "r", newline='' )
        data = csv.reader( source )
        with open( destfile, "w", newline='' ) as result:
            if settings.get( 'quoteall', True ):
                wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
            else:
                wtr = csv.writer( result )
            try:
                for row in data:
                    if debug:
                        loglines.extend( ['reading row',row] )
                    for column, transform in zip( columns, transforms ):
                        try:
                            oldfield = row[column]
                            do_transform = True
                        except IndexError as e:
                            do_tranform = False
                            loglines.append( 'invalid column number %s, ignorning' % str( column ) )
                        if do_transform:
                            new_field, tloglines = field_modules[transform.get( 'name' )].Transform( oldfield, transform, debug )
                            loglines.extend( tloglines )
                            if new_field:
                                row[column] = new_field
                    wtr.writerow( row )
                    if debug:
                        loglines.extend( ['writing row',row] )
            except UnicodeDecodeError:
                source.close()
                return False, ['field transforms failed while reading file ' + destfile, str( e )]
        source.close()
        loglines.append( 'field transforms complete' )
        return destfile, loglines
