import requests

def get_lat_long(address):
    """
    Uses the Nominatim API to get latitude and longitude for a given address.
    Returns a tuple (latitude, longitude) or (None, None) if not found.
    """
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        if data:
            lat = data[0].get('lat')
            lon = data[0].get('lon')
            return float(lat), float(lon)
        return None, None
    except (requests.RequestException, ValueError) as e:
        # Handle API or parsing error
        print(f"Error fetching geocode for address: {address}. Error: {e}")
        return None, None
