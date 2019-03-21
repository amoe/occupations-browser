import requests
import occubrow.errors

SELECT_ENDPOINT = "http://localhost:8090/api/query/select"

class MicromacroGateway(object):
    def query(self, query_data):
        headers = {}
        try:
            r = requests.post(SELECT_ENDPOINT, json=query_data, headers=headers)
            content = r.json()
            return content
        except requests.exceptions.ConnectionError as e:
            raise occubrow.errors.CannotContactMicromacroError(e)
    
        
