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

    def list_service(
        self,
        service,
        filter_field=None,
        filter_operator=None,
        filter_value=None,
        is_date_filter=False,
        sort_field=None,
        sort_order="ASC",
        limit=100,
    ):
        """
        Service current options are: "customers", "orders", "carts". \n
        Filter operation options = "!" not equal, "" equal, ">" greater than,"<" less than.\n
        Set is_date_filter to True if you are filtering a date field.
        """
        params = {"limit": limit, "display": "full"}
        if is_date_filter:
            params.update({"date": "1"})
        if filter_field and filter_operator is not None and filter_value:
            filter_value = filter_value.replace(" ", "%20")
            params.update({f"filter[{filter_field}]": f"{filter_operator}[{filter_value}]"})
        if sort_field:
            sort = {"sort": f"[{sort_field}_{sort_order}]"}
            params.update(sort)
        if service == "customers":
            return self.get("customers/", params=params)
        elif service == "orders":
            return self.get("orders/", params=params)
        elif service == "carts":
            return self.get("carts/", params=params)
        else:
            return f"No {service} service available for search"

    def list_inactive_carts(self, inactive_before, inactive_from=None, sort_field=None, sort_order="ASC", limit=100):
        """ 
        Checks all carts without an order and inactive before parameter 'inactive_before'. \n
        If 'inactive_from' is added, it will check inactive carts between inactive_from and inactive_before time. \n
        inactive_before and inactive_from format must be: 2023-02-13 13:31:28 (string). \n
        Sort order only works if sort_field is added. 
        """
        params = {
            "limit": limit,
            "display": "full",
            "date": 1,
            "filter[id_address_delivery]": "[0]",
            "filter[id_address_invoice]": "[0]",
        }
        if sort_field:
            sort = {"sort": f"[{sort_field}_{sort_order}]"}
            params.update(sort)
        if inactive_from:
            inactive_before = inactive_before.replace(" ", "%20")
            inactive_from = inactive_from.replace(" ", "%20")
            params.update({f"filter[date_add]": f"[{inactive_from},{inactive_before}]"})
        else:
            filter_value = inactive_before.replace(" ", "%20")
            params.update({f"filter[date_add]": f"<[{filter_value}]"})
        return self.get("carts/", params=params)

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
        params_string = "?"
        for param in self.params:
            params_string += f"{param}={self.params[param]}&"
        return requests.request(method, self.URL + endpoint + params_string[:-1], **kwargs)

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
