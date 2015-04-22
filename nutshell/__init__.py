import json
import requests
from uuid import uuid4

class NutshellApiException(Exception):
    pass

class NutshellAPI(object):
    DISCOVERY_ENDPOINT = u'https://api.nutshell.com/v1/json'

    def __init__(self, username, apikey):
        session = requests.Session()
        session.auth = (username, apikey)
        self.session = session

        self.user_endpoint = self._api_endpoint_for_user(username)

    def __getattr__(self, name):
        def wrapper(**kwargs):
            return self.json_rpc(
                url=self.user_endpoint,
                method=name,
                params=kwargs,
            )
        return wrapper

    def json_rpc(self, url, method, params={}):
        if not isinstance(url, basestring):
            raise NutshellApiException("Invalid url '%s'" % url)
        elif not isinstance(method, basestring):
            raise NutshellApiException("Invalid method '%s'" % method)
        elif not isinstance(params, dict):
            raise NutshellApiException('Invalid params, must be a dictionary')

        payload = {
            'method': method,
            'params': params,
            'id': self._generate_request_id(),
        }

        response = self.session.post(url, data=json.dumps(payload))

        if response.status_code != 200:
            raise NutshellApiException('HTTP status %s while finding endpoint: %s' % (
                response.status_code,
                url,
            ))

        data = response.json()

        if data["error"]:
            raise NutshellApiException(data["error"]["message"])

        return data["result"]

    def _api_endpoint_for_user(self, username):
        data = self.json_rpc(
            url=NutshellAPI.DISCOVERY_ENDPOINT,
            method='getApiForUsername',
            params={'username': username}
        )

        return 'https://' + data["api"] + '/api/v1/json'

    def _generate_request_id(self):
        return unicode(uuid4())
