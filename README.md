# VivialConnect Python Client Library

VivialConnect is a simple SMS/MSS API. It's designed specifically for developers seeking a simple, affordable and scalable messaging solution.

Get your API key here: https://www.vivialconnect.net/register <br>
Be sure to read the API documentation: https://www.vivialconnect.net/docs <br>
Library documentation lives here: https://vivialconnect.github.io/vivialconnect-python/


Requirements
------------

* [Requests](http://docs.python-requests.org/en/latest/)
* [six](https://pypi.python.org/pypi/six)

Installation
------------

You can install vivialconnect via pip with:

    pip install vivialconnect

Alternatively, you can clone the VivialConnect Python client repository:

    git clone https://github.com/VivialConnect/vivialconnect-python

Install:

    python setup.py install

Import the VivialConnect client:

    import vivialconnect

Examples
--------

```python
from vivialconnect import Resource, Message

Resource.api_key = "my-api-key"
Resource.api_secret = "my-api-secret"
Resource.api_account_id = "123456"

def send_message(to_number=None, from_number=None, body=None):
    message = Message()
    message.from_number = from_number
    message.to_number = to_number
    message.body = body
    message.send()

send_message(to_number='+11234567890',
             from_number='+19132597591',
             body='Howdy, from Vivial Connect!')
```

```python
from vivialconnect import Resource, Number

Resource.api_key = "my-api-key"
Resource.api_secret = "my-api-secret"
Resource.api_account_id = "123456"

def buy_number(name=None, phone_number=None, area_code=None, phone_number_type='local'):
    number = Number()
    number.name = name
    number.phone_number = phone_number
    number.area_code = area_code
    number.phone_number_type = phone_number_type
    number.buy()

buy_number(name='(913) 259-7591',
           phone_number='+19132597591',
           area_code='913',
           phone_number_type='local')
```

```python
from vivialconnect import Resource, Number

Resource.api_key = "my-api-key"
Resource.api_secret = "my-api-secret"
Resource.api_account_id = "123456"

def list_available_numbers(country_code='US', number_type='local',
                           area_code='913', in_postal_code=None,
                           in_region=None, limit=5):
    numbers = Number.available(
        country_code=country_code,
        number_type=number_type,
        area_code=area_code,
        in_postal_code=in_postal_code,
        in_region=in_region,
        limit=limit)
    for number in numbers:
        print("{} {} {}".format(number.name,
                                number.phone_number_type,
                                number.phone_number))

list_available_numbers()
```

Documentation
-------------

For up-to-date documentation visit: https://vivialconnect.github.io/vivialconnect-python/
