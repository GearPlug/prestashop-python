import requests

from prestashop.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    def __init__(self, webservice_key, domain, is_subfolder: bool = False, ssl_certificate: bool = False):
        protocol = "https" if ssl_certificate else "http"
        sub_url = "prestashop/api/" if is_subfolder else "api/"
        self.URL = f"{protocol}://{domain}/{sub_url}"
        self.params = {"output_format": "JSON", "ws_key": webservice_key}

    def check_api_features(self):
        return self.get("")

    def list_customers(
        self,
        filter_field=None,
        filter_operator=None,
        filter_value=None,
        is_date_filter=False,
        sort_field=None,
        sort_order="ASC",
        limit=100,
    ):
        params = {"limit": limit, "display": "full"}
        if is_date_filter:
            params.update({"date":"1"})
        if filter_field and filter_operator and filter_value:
            filter_value = filter_value.replace(" ", "%20")
            params.update({f"filter[{filter_field}]": f"{filter_operator}[{filter_value}]"})
        if sort_field:
            sort = {"sort": f"[{sort_field}_{sort_order}]"}
            params.update(sort)
        return self.get("customers/",params=params)

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
        params_string ="?"
        for param in self.params:
            params_string += f"{param}={self.params[param]}&"
        return requests.request(method, self.URL + endpoint + params_string[:-1], **kwargs)

    def parse(self, response):
        print(response.request.url)
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
