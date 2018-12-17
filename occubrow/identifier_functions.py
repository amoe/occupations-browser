import uuid

# An identifier function should take no arguments and return a string

def random_uuid():
    return str(uuid.uuid4())
