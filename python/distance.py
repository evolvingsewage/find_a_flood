""" Author : Carl Perez
    Description : Gets the nearest river info of a category
"""
import database
import requests
from geopy.geocoders import Nominatim
from math import degrees, sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
RADIUS_EARTH = 6373.0

def convert_km_to_mi(km):
    """ convert kilometers to miles
    Args:
        km - kilometers to be converted
    Returns:
        mi - the converted values
    """
    mi = 0.621371 * float(km)
    return mi


def compare_long_lat(coords, category="Major_Stage"):
    """ Gives the kilometer distance between a point and all rivers of
        a category, using derivation of haversine formula from:
        https://andrew.hedges.name/experiments/haversine/
    Args:
        coords - a tuple containing coords, lat then long
        category - a category of river flooding stage
    Returns:
        distances - a dictionary matching river coords to the distance from city
    """
    # init vars
    lat_point, lon_point = coords
    lat_point = radians(abs(lat_point))
    lon_point = radians(abs(lon_point))
    distances = {}

    # thanks andrew hedges, this saved me a ton of time
    for lat_river, lon_river in database.collect_coord(category):
        deg_lat_river = lat_river
        deg_lon_river = lon_river
        lat_river = radians(abs(lat_river))
        lon_river = radians(abs(lon_river))
        d_lon = lon_river - lon_point
        d_lat = lat_river - lat_point
        side_a = (sin(d_lat / 2)**2 + cos(lat_point) * \
                  cos(lat_river) * sin(d_lon / 2)**2)
        side_c = 2 * atan2(sqrt(side_a), sqrt(1 - side_a))

        distance = RADIUS_EARTH * side_c
        distance = convert_km_to_mi(distance)
        distances[(deg_lat_river, deg_lon_river)] = distance

    return distances


def get_city_coord(city, state):
    """ Get the coordinates of a US city using geopy
    Args:
        city - the city name
        state - the state abbrev.
    Returns:
        coords - the coordinates of the city
    """
    geolocator = Nominatim(user_agent="find_a_flood")
    location = geolocator.geocode("{0}, {1}".format(str(city), str(state)))
    coords = float(location.latitude), float(location.longitude)
    return coords


def get_rivers_within_dist(city, state, radius, category="Major_Stage"):
    """ Get the name of the rivers within a category within a specified distance
    Args:
        city - the city name
        state - the state abbrev.
        radius - the specified distance range in miles
        category - a category of a river flooding stage
    Returns:
        rivers - a dictionary with rivers containing info from database and
                 distance from city
    """
    distances = compare_long_lat(get_city_coord(city, state))

    for river_coords, distance in distances.items():
        if distance > float(radius):
            print("{0} < {1}".format(distance, radius))
            print(database.select_where_coord(str(river_coords), category))
    return

get_rivers_within_dist("Shreveport", "LA", 50)
