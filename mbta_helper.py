import urllib.request
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "4piLQbWbk4ruiwYv6BxmKeJUQQi3Lkap"
MBTA_API_KEY = "b6cfab58792c4ac58b111bcd2e717ff1"


# A little bit of scaffolding if you want to use it


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    pprint(response_data)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    place_name_valid = place_name.replace(" ", "%20")
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name_valid}'
    response_data = get_json(url)
    displayLatLng = response_data["results"][0]["locations"][0]['displayLatLng']
    lat = displayLatLng["lat"]
    ltt = displayLatLng["lng"]
    with open(f'mppp.json', 'w') as file:
        file.write(json.dumps(response_data, indent=1))
    return (lat, ltt)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url = f'https://api-v3.mbta.com/stops?sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}&filter%5Bradius%5D=0.3'
    info = get_json(url)
    station_name = info['data'][0]['attributes']['name']
    wheelchair_boarding = info['data'][0]['attributes']['wheelchair_boarding']
    return (station_name, wheelchair_boarding)


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    address = get_lat_long(place_name)
    info = get_nearest_station(address[0], address[1])
    wheelchair_accessible = ""
    wheelchair_boarding = info[1]

    if wheelchair_boarding == 0:
        wheelchair_accessible = "No Information"
    elif wheelchair_boarding == 1:
        wheelchair_accessible = "Accessible"
    else:
        wheelchair_accessible = "Inaccessible"
    return (info[0], wheelchair_accessible)


def main():
    """
    You can test all the functions here
    """
    print(get_lat_long("babson college"))
    print(get_nearest_station(42, -71))
    print(find_stop_near("wellesley college"))


if __name__ == '__main__':
    main()
