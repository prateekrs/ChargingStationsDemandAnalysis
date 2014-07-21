import sys
sys.path.append('my_libraries')
from squaremaker import make_grid
from filemanage import load_json, get_directories, render_file_style

import argparse
import textwrap
import sys, os
import json
import numpy as np
import pymongo
from os.path import join, exists

from shapely.geometry import shape, Point, MultiPoint

datadir, resultsdir = get_directories()

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
            type=float,
            help='county grid size - enter as an integer')

        return parser

def make_charging_station_dict(charging_stations):
    charge_dict = {}

    f = open(charging_stations, 'r')

    data = f.readlines()

    for row in data[1:]:
        i = row.split(',')
        id_num = i[1]
        time = i[2]
        usage = i[3]
        lat = float(i[4])
        lon = float(i[5].replace('\n', ""))

        charge_dict[id_num] = (lon, lat)

    return charge_dict







class RadiusMaker(object):
        """Aggregates variables to make a grid.



    Attributes:
      square_size (int): 
      county_name (str):
      features (Cursor): data removed from mongodb
      self.xgrid, self.ygrid (lists of floats):
      self.property_codes (dict): property codes as defined in file....
      dct (dict):
          grid_dct (dict):

    """

        def __init__(self, radius_size, county_name, features, charging_stations):
                self.radius_size = radius_size
                self.county_name = county_name

                self.features = features

                self.dct = {}
                self.grid_dct = {}

                self.property_codes = load_json(datadir + '/property_types_json/building_to_types.json')

                self.charging_stations = charging_stations
                self.count_in_buffer()

        def buffer_point(self, point):
            buffer = point.buffer(self.radius_size)
            blocks = buffer
            return blocks

        def count_in_buffer(self):

            for station in self.charging_stations:
                x, y =  self.charging_stations[station]

                point = Point(x, y)
                
                buffered_point = self.buffer_point(point)
                
                # return len([p for p in points.geoms if buffered_point.contains(p)])








def main(sys_args):
        parser = _build_parser(sys_args[0])
        args = parser.parse_args(sys_args[1:])

        radius_size = args.radius_size
        county_name = args.county_name
        features = load_json('/Users/mattstringer/research/Houston_analysis/houston_short.json')

        charging_stations = join(datadir, 'charging_stations', render_file_style(county_name), 'DC_charging_stations_MonthlyDemand.csv')

        if exists(charging_stations):
            charging_stations = make_charging_station_dict(charging_stations)

            r = RadiusMaker(radius_size, county_name, features, charging_stations)



        print('Done.')  



if __name__ == '__main__':
    sys.exit(main(sys.argv))