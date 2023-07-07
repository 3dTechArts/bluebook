"""
The `config` module provides the basic package configurations, including paths and coloring styles.

Module: baseconfig.py
Author: Reza Mousavi (reza.mousavii@gmail.com)

Configuration Constants:
    BASE_PATH (str): The base path of the package.
    DATABASE_DIR (str): The directory path for the database.
    JSON_DATABASE_FILE (str): The file path for the JSON database.
    LIB_DIR (str): The directory path for the package's library.
    API_DIR (str): The directory path for the package's code.
    EXPORTS_DIR (str): The directory path for the exports.
    TEST_UNIT_DIR (str): The directory path for the test units.

Styling Dictionary:
    styling (dict): A dictionary containing different color codes for styling text output.

Usage:
    # Importing the config module
    import config

    # Accessing configuration constants
    database_file = config.JSON_DATABASE_FILE
    library_directory = config.LIB_DIR

    # Accessing styling colors
    cyan_color = config.styling["CYAN"]
    red_color = config.styling["RED"]

"""

import os

#Please modify according to the path you have copied the package
BASE_PATH = '/your/new/path/bluebook/'

#Declaring database directory and file names
DATABASE_DIR = os.path.join(BASE_PATH, 'database/')
JSON_DATABASE_FILE = os.path.join(DATABASE_DIR, 'phonebook.json')

#Declaring other package paths 
LIB_DIR = os.path.join(BASE_PATH, 'lib/')
API_DIR = os.path.join(BASE_PATH, 'api/')
EXPORTS_DIR = os.path.join(BASE_PATH, 'exports/')
TEST_UNIT_DIR = os.path.join(BASE_PATH, 'test/')



# slyling is used to colorize different parts of texts which get printed on the screen
styling = {
    "CYAN"   	: '\033[96m',
    "BROWN"  	: '\033[0;33m',
    "RED"    	: '\033[0;91m',
    "PURPLE" 	: '\033[0;35m',
    "BOLD"   	: '\033[1m',
    "END"    	: '\033[0m',
    "WHITE"  	: '\033[0;47m',
    "GRAY"  	: '\033[0;47m',
    "UNDERLINE" : '\033[2;47m',
    "BLINK"     : '\033[5m',
    "ORANGE"    : '\033[38;5;208m',
    "GREEN"     : '\033[38;5;46m',
    "GREEN1"    : '\033[92m',
    "YELLOW"    : '\033[38;5;11m'
    }


