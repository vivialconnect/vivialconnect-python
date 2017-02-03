Vivial Connect
--------------

Vivial Connect is a solution set specifically for developers looking for a simple,
affordable and scalable messaging solution. Vivial Connect supports rapid development
and deployment. Our API platform supports various mobile messaging needs, enabling
developers to easily and affordably send and receive communications for any application.

Our API is Fun
``````````````

Save code to ``example.py`` file:

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

And Easy to Setup
`````````````````

Update your credentials, and run it:

.. code:: bash

    $ pip install vivialconnect
    $ python example.py

Links
`````

* `website <https://www.vivialconnect.net/>`_
* `documentation <https://www.vivialconnect.net/docs/>`_
* `development version
  <https://github.com/vivialconnect/vivialconnect-python>`_
