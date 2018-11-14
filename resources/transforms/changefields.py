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
        transforms = settings.get( 'transforms' )
        if not transforms:
            return False, ['no transforms provided for field transforms module']
        tcolumns = []
        for transform in transforms:
            tcolumn = transform.get( 'column' )
            if tcolumn == None:
                return False, ['column information not included in transform setting']
            else:
                tcolumns.append( tcolumn )
        encoding = settings.get( 'encoding' )
        if encoding:
            source = open( orgfile, "r", newline='', encoding=encoding )
        else:
            source = open( orgfile, "r", newline='' )
        if debug:
            loglines.extend( ['column list is:', tcolumns, 'transform list is:', transforms] )
        data = csv.reader( source )
        with open( destfile, "w", newline='' ) as result:
            if settings.get( 'quoteall', True ):
                wtr = csv.writer( result, quoting=csv.QUOTE_ALL )
            else:
                wtr = csv.writer( result )
            try:
                for row in data:
                    newrow = []
                    for i in range(0, len( row )):
                        oldfield = row[i]
                        if i in tcolumns:
                            for check_transform in transforms:
                                if check_transform.get( 'column' ) == i:
                                    transform = check_transform
                                    break
                            transform['fullrow'] = row
                            newfield, tloglines = field_modules[transform.get( 'name' )].Transform( oldfield, transform, debug )
                            loglines.extend( tloglines )
                            if not newfield is None:
                                if not isinstance( newfield, list ):
                                    newrow.append( newfield )
                                else:
                                    for anewfield in newfield:
                                        newrow.append( anewfield )
                        else:
                            newrow.append( oldfield )
                    wtr.writerow( newrow )
            except UnicodeDecodeError:
                source.close()
                return False, ['field transforms failed while reading file ' + destfile, str( e )]
        source.close()
        loglines.append( 'field transforms complete' )
        return destfile, loglines
