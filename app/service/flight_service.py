import requests

def get_flight():
    url = "https://opensky-network.org/api/states/all"
    try:
        # Add a timeout to prevent the server from hanging and crashing
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching flights: {e}")
        # Return an empty structure if the API fails so the frontend doesn't crash
        return {"states": []}