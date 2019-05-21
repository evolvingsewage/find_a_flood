""" Author : Carl Perez
    Description : Parses the river data into something a human can use
"""
import os
import subprocess
import xml.etree.ElementTree as ET
from os import chdir, getcwd

# define constants
THIS_DIR = getcwd()

def download_river_data():
    """ Use BASH to download river data
    Args:
        none
    Returns:
        none
    """
    subprocess.check_call("bash ../bash/river.sh", shell=True)
    return None


def import_riverobs(resync=False):
    """ Using the Python xml library to create an navigatable object
    Args:
        resync - whether or not to re-download data
                 THIS HAS SIGNIFICANT PERFORMANCE EFFECTS
    Returns:
        xml_obj - a navigatable XML object
    """
    if resync:
        download_river_data()
    tree = ET.parse(os.path.join(THIS_DIR, "riverOBS.xml"))
    root = tree.getroot()
    return root


def clean_category_data(category):
    """ Get all the flooding information from a category
    Args:
        category - the xml element containing rivers of a category
    Returns:
        rivers_dict - all the rivers in a category in a dictionary
    """
    clean_category_dict = {}
    for river in category.iter("Placemark"):
        # retrieve elements as strings and format
        river_name = river.find("name")
        river_ds = ET.tostring(river.find("description"))
        river_coord = river.find("Point")
        # remove those annoying zeros
        river_coord = "".join(river_coord.itertext()).strip().strip("0")
        river_coord = ", ".join(reversed(river_coord.split(", "))).strip("0")
        river_name = "".join(river_name.itertext()).strip()

        # place in dict
        clean_category_dict[river_name] = {}
        #TODO: parse HTML here for a full dict
        clean_category_dict[river_name]["description"] = "it's a river"
        clean_category_dict[river_name]["coordinates"] = river_coord
    return clean_category_dict


def clean_xml_data(parsed_data):
    """ Clean up data for use in a dictionary
        DO NOT THROW RAW XML STUFF HERE, IT WILL NOT WORK
    Args:
        parsed_data - the parsed data set (created by import_riverobs, ideally)
    Returns:
        clean_river_data - river data in a dictionary for ease of navigation
    """
    clean_river_data = {}
    for element in parsed_data.iter("Folder"):
        category_string = element.find("name")
        # if it is actually a category, create a dict for it
        if category_string is not None:
            category_string = "".join(category_string.itertext())
            clean_river_data[category_string] = clean_category_data(element)
        else:
            continue
    return clean_river_data
