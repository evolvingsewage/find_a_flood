""" Author : Carl Perez
    Description : Creates and interacts with a database of the river information
"""
import parse
import re
import sqlite3
import subprocess
from itertools import chain

def create_db_cursor():
    """ Create DB cursor
    Args:
        None
    Returns:
        connection, db_cursor
    """
    connection = sqlite3.connect("flooding_info.db")
    return (connection, connection.cursor())


def scrub_table_name(table_name):
    """ Remove potential injection from strings so one can use vars
        as table names
    Args:
        table_name - the desired table name
    Returns:
        a clean string
    """
    table_name = re.sub(r"\s+", "_", table_name)
    return ''.join( chr for chr in table_name if chr.isalnum() or chr == "_" )


def init_river_db(resync=False):
    """ Create and populate the river database
    Args:
        resync - whether or not to re-download data
                 THIS HAS SIGNIFICANT PERFORMANCE EFFECTS

    Returns:
        success - whether or not the init succeeded
    """
    # parse raw data
    raw_river_data = parse.import_riverobs(resync)
    river_data = parse.clean_xml_data(raw_river_data)

    # init blank db and cursor
    connection, db_cursor = create_db_cursor()

    # build and populate tables
    for category, river_info in river_data.items():
        c_cat = scrub_table_name(category)
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS {0}(RIVER TEXT,
                             DESCRIPTION TEXT,COORD TEXT)'''.format(c_cat))
        for name, info in river_info.items():
            clean_info = (name, info["description"], info["coordinates"])
            db_cursor.execute('''INSERT INTO {0} VALUES (?,?,?)
                              '''.format(c_cat), clean_info)

    # commit & close
    connection.commit()
    connection.close()


def collect_coord(category):
    """ Collect all the coordinates in the database of a category
    Args:
        category
    Returns:
        coords - a list of tuples of all the coords
    """
    # db connection init
    connection, db_cursor = create_db_cursor()
    c_cat = scrub_table_name(category)

    # pull list of coords and turn into tuples
    coords = []
    raw_coords = db_cursor.execute(''' SELECT COORD FROM {0}'''.format(c_cat))
    for coord in raw_coords:
        coord = tuple(map(float, "".join(coord).split(",")))
        coords.append(coord)
    return coords


def select_where_coord(coordinates, category):
    """ Select rivers with the coordinates specified in a category
    Args:
        coordinates - a string of coordinates
    Returns:
        river_info
    """
    # db connection init
    connection, db_cursor = create_db_cursor()
    c_cat = scrub_table_name(category)

    # a lot of ugly conversions, first removing fluff from string and turning to a list
    # then mapping all the strings in the list into floats, then making the list a tuple
    # THEN FINALLY making that tuple safe for use in SQL
    clean_coords = tuple(map(float, coordinates.lstrip().strip("(,)").split(", ")))
    clean_coords = (", ".join(map(str, clean_coords)),)

    river_info = db_cursor.execute(''' SELECT * FROM {0} WHERE COORD=? '''.format(c_cat),
                                   clean_coords)
    return river_info.fetchone()
