""" Author : Carl Perez
    Description : Parses the river data into something a human can use
"""
import json
import os
import requests
from os import getcwd

# define constants
THIS_DIR = getcwd()

# NOAA retired the old AHPS KMZ download in favor of this ArcGIS feature
# service, which serves the same river gauge data as paginated GeoJSON.
NWPS_GAUGE_QUERY_URL = ("https://mapservices.weather.noaa.gov/eventdriven/"
                        "rest/services/water/riv_gauges/MapServer/0/query")
PAGE_SIZE = 2000


def download_river_data():
    """ Download all river gauge data from NOAA's NWPS feature service
    Args:
        none
    Returns:
        none
    """
    features = []
    offset = 0
    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "false",
            "resultRecordCount": PAGE_SIZE,
            "resultOffset": offset,
            "f": "geojson",
        }
        response = requests.get(NWPS_GAUGE_QUERY_URL, params=params, timeout=30)
        response.raise_for_status()
        page = response.json()["features"]
        if not page:
            break
        features.extend(page)
        offset += len(page)

    with open(os.path.join(THIS_DIR, "riverOBS.json"), "w") as river_file:
        json.dump(features, river_file)
    return None


def import_riverobs(resync=False):
    """ Load the river gauge data, downloading it first if needed
    Args:
        resync - whether or not to re-download data
                 THIS HAS SIGNIFICANT PERFORMANCE EFFECTS
    Returns:
        features - a list of GeoJSON feature dicts
    """
    river_file_path = os.path.join(THIS_DIR, "riverOBS.json")
    if resync or not os.path.exists(river_file_path):
        download_river_data()
    with open(river_file_path) as river_file:
        return json.load(river_file)


def clean_xml_data(features):
    """ Group gauge features by flood category
    Args:
        features - the list of GeoJSON feature dicts (from import_riverobs)
    Returns:
        clean_river_data - all rivers grouped by category in a dictionary
    """
    clean_river_data = {}
    for feature in features:
        props = feature["properties"]
        category = props["status"]
        river_name = props["waterbody"] or props["gaugelid"]
        coordinates = "{0}, {1}".format(props["latitude"], props["longitude"])

        clean_river_data.setdefault(category, {})
        clean_river_data[category][river_name] = {
            "description": "it's a river",
            "coordinates": coordinates,
        }
    return clean_river_data
