import re

def collapse(qry):
    return re.sub(r'\s+', ' ', qry)
