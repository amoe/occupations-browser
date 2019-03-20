


def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False
    
    
