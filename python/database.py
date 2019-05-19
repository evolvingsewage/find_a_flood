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
        db_cursor
    """
    connection = sqlite3.connect("flooding_info.db")
    return connection.cursor()


def download_river_data():
    """ Use BASH to download river data
    Args:
        none
    Returns:
        none
    """
    subprocess.check_call("bash ../bash/river.sh", shell=True)
    return None

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
    if resync:
        download_river_data()

    # parse raw data
    raw_river_data = parse.import_riverobs()
    river_data = parse.clean_xml_data(raw_river_data)

    # init blank db and cursor
    db_cursor = create_db_cursor()

    # build and populate tables
    for category, river in river_data.items():
        c_cat = scrub_table_name(category)
        db_cursor.execute('''CREATE TABLE {}(RIVER TEXT, DESCRIPTION TEXT,
                             COORD TEXT)'''.format(c_cat))

init_river_db()
