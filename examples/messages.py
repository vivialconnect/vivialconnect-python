from vivialconnect import Message


def send_message(to_number=None, from_number=None, body=None):
    message = Message()
    message.from_number = from_number
    message.to_number = to_number
    message.body = body
    message.send()


def list_messages():
    count = Message.count()
    messages = Message.find()
    for message in messages:
        print(message.id, message.to_number,
              message.from_number, message.body)


def get_message(id):
    message = Message.find(id)
    print(message.id, message.to_number,
              message.from_number, message.body)
