from vivialconnect import Configuration


def list_configurations():
    configs = Configuration.find()
    for config in configs:
        yield config


def create_configuration(name=None,
                         phone_number=None,
                         phone_number_type=None,
                         message_status_callback=None,
                         sms_url=None,
                         sms_method=None,
                         sms_fallback_url=None,
                         sms_fallback_method=None):
    config = Configuration()
    config.name = name
    config.phone_number = phone_number
    config.phone_number_type = phone_number_type
    config.message_status_callback = message_status_callback
    config.sms_url = sms_url
    config.sms_method = sms_method
    config.sms_fallback_url = sms_fallback_url
    config.sms_fallback_method = sms_fallback_method
    config.save()
    return config


def get_configuration(id):
    config = Configuration.find(id)
    return config


def delete_configuration(id):
    config = Configuration.find(id)
    config.destroy()
    return True
