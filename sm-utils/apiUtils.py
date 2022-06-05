import requests

def send_request_to_api(DATA, URL, CONTENT_TYPE=None, ACCEPT_TYPE=None, API_KEY=None):
    HEADERS = {}
    if CONTENT_TYPE is not None:
        HEADERS['Content-Type'] = CONTENT_TYPE
        HEADERS['ContentType'] = CONTENT_TYPE
    if ACCEPT_TYPE is not None:
        HEADERS['Accept'] = ACCEPT_TYPE
    if API_KEY is not None:
        HEADERS['X-API-Key'] = API_KEY

    return requests.request(method='GET', url=URL, headers=HEADERS, data=DATA)
