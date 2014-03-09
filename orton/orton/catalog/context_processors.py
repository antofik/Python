from catalog.models import options

def catalog(request=None):
    values = {}
    for p in options:
        values[p[0]] = p[1]
    return values
