from vivialconnect import Number


def list_associated_numbers():
    numbers = Number.find()
    for number in numbers:
        yield number

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
        yield number


def buy_number(name=None, phone_number=None,
               area_code=None, phone_number_type='local'):
    number = Number()
    number.name = name
    number.phone_number = phone_number
    number.area_code = area_code
    number.phone_number_type = phone_number_type
    number.buy()
    return number


def update_number_name(id, name=None):
    number = Number.find(id)
    number.name = name
    number.save()
    return number
