""" Author : Carl Perez
    Description : Creates and interacts with a database of the river information
"""
import parse
import re
import sqlite3
import subprocess

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
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS {}(RIVER TEXT,
                             DESCRIPTION TEXT,COORD TEXT)'''.format(c_cat))
        for name, info in river_info.items():
            clean_info = (name, info["description"], info["coordinates"])
            db_cursor.execute('''INSERT INTO {} VALUES (?,?,?)
                              '''.format(c_cat), clean_info)
