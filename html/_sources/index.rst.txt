.. VivialConnect documentation master file, created by
    sphinx-quickstart on Mon Jan 16 15:42:51 2017.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to Vivial Connect's Python API documentation!
=====================================================

The Vivial Connect API library allows Python developers to programmatically
access the text messaging capabilities of the Vivial Connect service. In order
for API to communicate with the Vivial Connect REST web service, the data itself
is sent as JSON over HTTP.

Installation
------------

You can install vivialconnect via pip with::

    pip install vivialconnect

Alternatively, you can clone the VivialConnect Python client repository::

    git clone https://github.com/VivialConnect/vivialconnect-python

Install::

    python setup.py install

Import the VivialConnect client::

    import vivialconnect

Usage
-----

Getting Started
+++++++++++++++

Vivial Connect Python API uses ``request`` library to communicate with the
Vivial Connect REST web service. Before you start using Vivial Connect Python
API you will have to create an account on the www.vivialconnect.net web site.

In order to create a new account you can follow these steps:

* Go to www.vivialconnect.net and register for Vivial Connect service account.
* Reviewed the Vivial Connect API authentication process.
* Purchased a phone number from the list of available numbers.

After your account has been created and configured you can proceed with configuring
your Python application. This is a simple process. You will need following
information:

* account_id – Required – The Vivial Connect account ID
* api_secret – Required – The Vivial Connect API secret
* api_key – Required – The Vivial Connect API key

Now you're ready to make authorized API requests to your Vivial Connect account::

    from vivialconnect import Resource, Message

    Resource.api_account_id = "YOUR_ACCOUNT_ID"
    Resource.api_secret = "YOUR_API_SECRET"
    Resource.api_key = "YOUR_API_KEY"

    def send_message(to_number=None, from_number=None, body=None):
        message = Message()
        message.from_number = from_number
        message.to_number = to_number
        message.body = body
        message.send()
        return message

    def get_message(id):
        message = Message.find(id)
        return message

    # Send SMS
    message = send_message(to_number='+11234567890',
                           from_number='+19132597591',
                           body='Howdy, from Vivial Connect!')
    # Get dispatched SMS info
    message = get_message(message.id)
    print(message.id, message.to_number,
          message.from_number, message.body)

Limitations
+++++++++++

Currently Vivial Connect Python API doesn't support asynchronous requests.

Contents:

.. toctree::
    :maxdepth: 2

    api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
