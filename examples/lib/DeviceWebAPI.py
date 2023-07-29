import json
import requests
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class DeviceWebAPI:
    def __init__(self, conf):
        self.host = conf.get("host", "localhost")
        self.port = conf.get("port", 80)
        self.user = conf.get("username", "admin")
        self.password = conf.get("password", "baidnncam")
        self.auth = None
        self.endpoint=f"http://{self.host}:{self.port}/api/"

    def get_auth(self):
        if self.auth is None:
            response = requests.post(self.endpoint + "auth/login",json={'username' : self.user, 'password' : self.password},
                                        headers={'Content-Type': 'application/json'})
            if response.status_code != 200:
                log.error(f"Error in response to auth POST on {self.endpoint}")
                raise requests.HTTPError(response.status_code, response.content.decode(encoding='UTF-8'))
            self.auth = response.json()['Authorization']
        return self.auth

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization' : self.get_auth()
        }

    def request(self, method, url, params={}, data=[], json={}):
        """ request from device  API

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional) Dictionary or list fof tuples ``[(key, value)]`` (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.

        """
        headers = self.get_headers()
        response = requests.request(method=method, url=self.endpoint + url, params=params, data=data, json=json, headers=headers)
        return response

    def get_response(self, endpoint):
        """ GET request from device API

        Parameters
        ----------
        endpoint : str
            URL for request

        Returns
        -------
        data : dict
            JSON of response
        """

        log.debug(endpoint)
        headers = self.get_headers()
        response = requests.get(self.endpoint + endpoint, headers=headers)
        if response.status_code != 200:
            log.error(f"Error in response to GET on {endpoint} with headers {headers}")
            log.error(f"{response.status_code} : {response.content.decode()}")
            if response.status_code == 404:
                log.debug("Invalid endpoint. Check device ID and service name")
            raise requests.HTTPError(response.status_code, response.content.decode(encoding='UTF-8'))
        return response.json()


    def post_request(self, endpoint, json={}, params=None):
        """ POST request from device API

        Parameters
        ----------
        endpoint : str
            URL for request
        json : dict
            JSONifiable dict for POST request

        Returns
        -------
        data : dict
            JSON of response

        """
        log.debug(endpoint)
        log.debug(json)
        response = requests.post(self.endpoint + endpoint, json=json, headers=self.get_headers(), params=params)
        if response.status_code not in [200, 201, 202]:
            log.debug(f" POST {endpoint} = {response.status_code} : {response.content.decode()}")
            raise requests.HTTPError(response.status_code, response.content.decode(encoding='UTF-8'))
        return response.json()

    def put_request(self, endpoint, json={}, params=None):
        """ PUT request from device API

        Parameters
        ----------
        endpoint : str
            URL for request
        json : dict
            JSONifiable dict for POST request

        Returns
        -------
        data : dict
            JSON of response

        """
        log.debug(endpoint)
        log.debug(json)
        response = requests.put(self.endpoint + endpoint, json=json, headers=self.get_headers(), params=params)
        if response.status_code not in [200, 201, 202]:
            log.debug(f" PUT {endpoint} = {response.status_code} : {response.content.decode()}")
            raise requests.HTTPError(response.status_code, response.content.decode(encoding='UTF-8'))
        return response.json()

    def delete_request(self, endpoint, json=None):
        """ POST request from device API

        Parameters
        ----------
        endpoint : str
            URL for request
        json : dict
            JSONifiable dict for POST request

        Returns
        -------
        data : dict
            JSON of response

        """
        log.debug(endpoint)
        log.debug(json)
        response = requests.delete(self.endpoint + endpoint, json=json, headers=self.get_headers())
        # 204 corresponds to service/device uninstalled i.e service/device deleted
        if response.status_code != 204:
            log.debug(f"{response.status_code}")
            raise requests.HTTPError(response.status_code, response.content.decode())
        return response.content.decode()

    def patch_request(self, endpoint, json):
        """ PATCH request from device API

        Parameters
        ----------
        endpoint : str
            URL for request
        json : dict
            JSONifiable dict for PATCH request

        Returns
        -------
        data : dict
            JSON of response

        """
        log.debug(endpoint)
        log.debug(json)
        response = requests.patch(self.endpoint + endpoint, json=json, headers=self.get_headers())
        if response.status_code != 200:
            log.error("Error with response")
            log.error(f"{response.status_code} : {response.content.decode()}")
            return False
        return response.json()