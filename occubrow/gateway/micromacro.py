import requests

class MicromacroGateway(object):
    def query(query_data):
        r = requests.post(endpoint, json=postdata, headers=headers)
        content = r.json()
        return content
        
