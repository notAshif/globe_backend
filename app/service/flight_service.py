import requests

def get_flight():
    url = "https://opensky-network.org/api/states/all"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # OpenSky is often slow, 15s timeout
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        import traceback
        print(f"FAILED TO FETCH FLIGHTS: {type(e).__name__}: {e}")
        traceback.print_exc()
        return {"states": []}