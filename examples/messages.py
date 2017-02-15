from vivialconnect import Message


def send_message(to_number=None, from_number=None,
                 body=None, media_urls=None):
    message = Message()
    message.from_number = from_number
    message.to_number = to_number
    message.body = body
    message.media_urls = media_urls
    message.send()
    return message


def list_messages():
    count = Message.count()
    messages = Message.find()
    for message in messages:
        yield message


def get_message(id):
    message = Message.find(id)
    return message
