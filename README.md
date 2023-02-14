![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)
# prestashop-python

*prestashop-python* is an API wrapper for Prestashop, written in Python.
## Installing
```
pip install prestashop-python
```
## Usage
```
client = Client(webservice_key, domain, is_subfolder:bool=None, ssl_certificate:bool=None)
# domain : Don't include https:// prefix and trailing slash / ex:(mydomain.com)
```
### Check API features
```
response = client.check_api_features()
```
### List service (customers, orders and carts)
```
response = client.list_customers(service, filter_field=None, filter_operator=None, filter_value=None, is_date_filter=False,
                                 sort_field=None, sort_order="ASC", limit=100)
# Service current options are: "customers", "orders", "carts"
# Filter operation options = "!" not equal, "" equal, ">" greater than,"<" less than
# set is_date_filter to True if you are filtering a date field.
```
### List inactive carts
```
response = client.list_inactive_carts(inactive_before, inactive_from=None, sort_field=None, sort_order="ASC", limit=100)
# Checks all carts without an order and inactive before parameter 'inactive_before'.  
# If 'inactive_from' is added, it will check inactive carts between inactive_from and inactive_before time.  
# inactive_before and inactive_from format must be: 2023-02-13 13:31:28 (string).  
# Sort order only works if sort_field is added. 
```
