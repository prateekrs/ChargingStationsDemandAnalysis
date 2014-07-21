import sys
sys.path.append('my_libraries')
from squaremaker import make_grid
from filemanage import load_json, get_directories

import argparse
import textwrap
import sys, os
import json
import numpy as np
import pymongo



USAGE = textwrap.dedent("""\
        Create a dense data matrix from raw mixed features. U""")

def _build_parser(prog):
        """
        Used in main function. Allows items to be entered from the command line. It elminaates
        the use of hard coded items in the code.

        Args:
      county_name (string): The county name for the study area. Necessary for saving the files in the appropriate locations
      square_size (int): Used to 

    Returns:
      parser

        """

        parser = argparse.ArgumentParser(prog=prog, description=USAGE)
        parser.add_argument(
            '--county_name',
            required=True,
            type=str,
            help='Name of county that you are currently matching, \n example is "San Diego"')

        parser.add_argument(
            '--radius_size',
            required=True,
            type=int,
            help='county grid size - enter as an integer')

        return parser