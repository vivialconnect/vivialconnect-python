VivialConnect is a simple SMS/MMS API. It's designed specifically for developers seeking a simple, affordable and scalable messaging solution.

Register an API account here: https://www.vivialconnect.net and login to the website to buy your first phone number.

Setup is Easy!
--------------


Copy this code into a file named ``example.py``


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
                 from_number='+19876543210',
                 body='Howdy, from Vivial Connect!')


Update the API key, secret and account id. Change 'from_number' to the number you purchased. Then run it:

.. code:: bash

    $ pip install vivialconnect
    $ python example.py

Links
-----

* `Website <https://www.vivialconnect.net/>`_
* `Documentation <https://www.vivialconnect.net/docs/>`_
* `Development Version
  <https://github.com/vivialconnect/vivialconnect-python>`_
