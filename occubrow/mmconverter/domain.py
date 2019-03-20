def span_from_json(text_token):
    from_pos = text_token['from']
    to_pos = text_token['to']
    with_value = text_token['with']
    with_type = text_token['withType']

    return Span(from_pos, to_pos, with_value, with_type)

class Span(object):
    def __init__(self, from_pos, to_pos, with_value, with_type):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.with_value = with_value
        self.with_type = with_type

    def __repr__(self):
        return "<domain.Span({!r}, {!r}, {!r}, {!r})>".format(
            self.from_pos, self.to_pos, self.with_value, self.with_type
        )

# class DomainObject(object):
#     def __init__(self, freetext, 
