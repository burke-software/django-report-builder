
def javascript_date_format(python_date_format):
    format = python_date_format.replace(r'%Y', 'yyyy')
    format = format.replace(r'%m', 'mm')
    format = format.replace(r'%d', 'dd')
    if '%' in format:
        format = ''
    if not format:
        format = 'yyyy-mm-dd'
    return format

