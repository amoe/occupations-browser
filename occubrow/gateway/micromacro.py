import requests

SELECT_ENDPOINT = "http://localhost:8090/api/query/select"

class MicromacroGateway(object):
    def query(self, query_data):
        headers = {}
        r = requests.post(SELECT_ENDPOINT, json=query_data, headers=headers)
        content = r.json()
        return content
        
