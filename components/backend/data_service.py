CREATE_PARENT_SENTENCE_STATEMENT = """
    CREATE (s1:Sentence {tokens: {token_seq}})
"""

CREATE_TOKEN_STATEMENT = """
    CREATE (t1:Token {node_properties})
"""

import misc
import pprint

class DataService(object):
    def __init__(self):
        pass

    def create_occupation_description_from_tokens(self, token_seq):
        result = misc.run_some_query(
            CREATE_PARENT_SENTENCE_STATEMENT, {'token_seq': token_seq}
        )

        for index, value in enumerate(token_seq):
            node_properties = {'index': index}

            if index == 0:
                node_properties['firstToken'] = True
            elif index == len(token_seq) - 1:
                node_properties['lastToken'] = True

            pprint.pprint(node_properties)

            misc.run_some_query(
                CREATE_TOKEN_STATEMENT, {'node_properties': node_properties}
            )

                
        return result
