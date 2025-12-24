import requests

def get_params(season,seasonType,week):
    params = {
        "season":season,
        "seasonType":seasonType,
        "week":week
    }
    return params

def get_headers():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://nextgenstats.nfl.com",
    }
    return headers

def get_data(url,params):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://nextgenstats.nfl.com",
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

def get_leaders(data):
    leaders = data["leaders"]
    return leaders