Vivial Connect
--------------

VivialConnect is a simple SMS/MSS API. It's designed specifically for developers seeking a simple, affordable and scalable messaging solution.

Our API is Fun...
```````````````
Register an API account here: https://www.vivialconnect.net/register and login to the website to buy your first phone number.

To test, copy this code to a file named ``example.py``

.. code:: python

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


And Easy to Setup!
`````````````````

Update the API key, secret and account id. Change 'from_number' to the number you purchased. Then run it:

.. code:: bash

    $ pip install vivialconnect
    $ python example.py

Links
`````

* `website <https://www.vivialconnect.net/>`_
* `documentation <https://www.vivialconnect.net/docs/>`_
* `development version
  <https://github.com/vivialconnect/vivialconnect-python>`_
