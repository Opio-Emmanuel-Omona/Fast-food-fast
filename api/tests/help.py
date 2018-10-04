from flask import json

class HelpAPI():
    def __init__(self):
        pass
    # Helper methods for json tests
    def post_json(self, client, url, json_dict):
        return client.post(
            url,
            data=json.dumps(json_dict))

    def post_json_with_token(self, client, url, json_dict, token):
        return client.post(
            url,
            data=json.dumps(json_dict),
            headers=dict(
                Authorization='Bearer ' + token
            )
        )

    def put_json_with_token(self, client, url, json_dict, token):
        return client.put(
            url,
            data=json.dumps(json_dict),
            headers=dict(
                Authorization='Bearer ' + token
            )
        )

    def put_json(self, client, url, json_dict):
        return client.put(
            url,
            data=json.dumps(json_dict))

    def delete_json(self, client, url):
        return client.delete(url)

    def json_of_response(self, response):
        return json.loads(response.data.decode('utf8'))

    # END helper methods