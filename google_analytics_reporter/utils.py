import uuid


def get_client_id(request):
    _ga = request.COOKIES.get('_ga')
    if _ga:
        ga_split = _ga.split('.')
        client_id = '.'.join((ga_split[2], ga_split[3]))
    else:
        client_id = uuid.uuid4()
    return client_id
