import os
import requests
from geopy.distance import geodesic

def get_current_location():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    address = "Plac Konesera, Warszawa, PL"  # Use a known valid address for testing
    endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(endpoint)
    geocode_result = response.json()

    if geocode_result['status'] == 'OK':
        location = geocode_result['results'][0]['geometry']['location']
        return (location['lat'], location['lng'])
    else:
        raise Exception(f"Geocoding failed with status: {geocode_result['status']} and error message: {geocode_result.get('error_message')}")

def get_disposal_locations(query="elektrosmieci"):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    current_location = get_current_location()
    lat, lng = current_location
    endpoint = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&keyword={query}&key={api_key}'
    response = requests.get(endpoint)
    places_result = response.json()

    if places_result['status'] == 'OK':
        locations = [
            {"name": place['name'], "location": (place['geometry']['location']['lat'], place['geometry']['location']['lng'])}
            for place in places_result['results']
        ]
        return locations
    else:
        raise Exception(f"Places query failed with status: {places_result['status']} and error message: {places_result.get('error_message')}")

def find_closest_disposal(current_location, disposal_locations):
    closest_location = min(disposal_locations, key=lambda loc: geodesic(current_location, loc['location']).miles)
    return closest_location

def get_shortest_route(origin, destination):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    params = {
        'origin': f"{origin[0]},{origin[1]}",
        'destination': f"{destination[0]},{destination[1]}",
        'key': api_key
    }
    response = requests.get(endpoint, params=params)
    directions = response.json()
    if directions['status'] == 'OK':
        route = directions['routes'][0]['legs'][0]
        return route['distance']['text'], route['duration']['text'], route['steps']
    else:
        raise Exception(f"Directions query failed with status: {directions['status']} and error message: {directions.get('error_message')}")

def main():
    current_location = get_current_location()
    disposal_locations = get_disposal_locations()
    closest_disposal = find_closest_disposal(current_location, disposal_locations)
    
    print(f"Closest disposal location: {closest_disposal['name']}")
    
    distance, duration, steps = get_shortest_route(current_location, closest_disposal['location'])
    
    if steps:
        print(f"Distance: {distance}, Duration: {duration}")
        for step in steps:
            print(step['html_instructions'])
    else:
        print("Could not retrieve route information")

if __name__ == "__main__":
    main()
