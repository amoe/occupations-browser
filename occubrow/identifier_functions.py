import uuid

# An identifier function should take no arguments and return a string

def random_uuid():
    return str(uuid.uuid4())

class PredictableUUIDGenerator(object):
    current_value = 0x00000000000000000000000000000000

    def __init__(self):
        pass

    def next(self):
        result = str(uuid.UUID(int=self.current_value))
        self.current_value += 1
        return result


def get_predictable_uuid_generator():
    obj = PredictableUUIDGenerator()
    return lambda: obj.next()
    

