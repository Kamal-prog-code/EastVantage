import geocoder
from requests import Response

def convert_address_coord(address: str):
    """Converts given address to latitude and longitude."""
    try:
        geolocator = geocoder.osm(address)
        address = geolocator.json['raw']['display_name']
        lat = geolocator.json['raw']['lat']
        lon = geolocator.json['raw']['lon']
        data = {
            "lat": lat,
            "long": lon, 
        }
        return data
    except Exception as e:
        return Response({"message":str(e)})