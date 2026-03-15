import requests

def get_flight():
    url = f"https://opensky-network.org/api/states/all"
    res = requests.get(url)
    return res.json()