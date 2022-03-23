import requests

def send_request_to_sm_endpoint(DATA, URL, METHOD, CONTENT_TYPE, ACCEPT_TYPE, API_KEY):
    HEADERS = {
        'ContentType': CONTENT_TYPE,
        'Accept': ACCEPT_TYPE,
        'Content-Type': CONTENT_TYPE,
        'X-API-Key': API_KEY
    }

    resp = requests.request(
        method=METHOD, 
        url=URL, 
        headers=HEADERS, 
        data=DATA
    )

    return resp.status_code, resp.content