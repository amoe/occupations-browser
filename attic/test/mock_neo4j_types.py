
# record wraps a 
class FakeRecord(object):
    def __init__(self, items):
        self.items = items

    def get(self, name):
        return items.get(name)


# The mocked structure will look something like the following, given that we
# only use two operations: iterating over the sequence, and getting a value from
# a node.  A BoltResultStatement maps to a list, a Path maps to a list, a Node 
# maps to a dictionary.
[
   {'seq': [{'content': 'foo', '_type': 'Token'}, {'content': 'bar', '_type': Token}],
    's1': {'_type': 'Sentence', 'content': ['foo', 'bar']}
]

class FakeBoltStatementResult(object):
    def __init__(self, seq):
        self.seq = seq

    def __iter__(self):
        return self.seq.__iter__()

    def __next__(self): 
        return self.seq.__next__()
