import requests
from config.config import config

def get_flight():
    api_key = config.FLIGHT_API_KEY
    url = f"https://airlabs.co/api/v9/flights?api_key={api_key}"
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        if "response" in data:
            mapped_states = []
            for flight in data.get("response", []):
                if flight.get("lat") and flight.get("lng"):
                    state = [
                        flight.get("hex", "N/A"),
                        flight.get("flight_icao", "N/A"),
                        flight.get("flag", "Unknown"),
                        None, None,
                        flight.get("lng"),
                        flight.get("lat"),
                        flight.get("alt", 0),
                        None,
                        flight.get("speed", 0) / 3.6,
                        flight.get("dir", 0)
                    ]
                    mapped_states.append(state)
            
            return {"states": mapped_states}
        
        return {"states": []}
        
    except Exception as e:
        print(f"AirLabs API Error: {e}")
        return {"states": []}