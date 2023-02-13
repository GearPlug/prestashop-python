import requests

from prestashop.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):

    def __init__(self, webservice_key, domain, is_subfolder:bool=False, ssl_certificate:bool=False):
        protocol = "https" if ssl_certificate else "http"
        sub_url = "prestashop/api/" if is_subfolder else "api/"
        self.URL = f"{protocol}://{domain}/{sub_url}"
        self.params = {"output_format": "JSON","ws_key": webservice_key}

    def check_api_features(self):
        return self.get("")

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, headers=None, params=None, **kwargs):
        if params:
            self.params.update(params)
        return requests.request(method, self.URL + endpoint, params=self.params, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
