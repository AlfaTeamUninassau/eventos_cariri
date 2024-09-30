import requests
from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API do OpenCage do arquivo .env
key = os.getenv('OPENCAGE_API_KEY')

def get_lat_long(address):
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(address)

    if result and len(result):
        lat = result[0]['geometry']['lat']
        lon = result[0]['geometry']['lng']
        return lat, lon
    return None, None