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
            help='charging station radius(in ft) size - enter a number')

        return parser

def make_charging_station_dict(charging_stations):
    charge_dict = {}

    f = open(charging_stations, 'r')

    data = f.readlines()

    for row in data[1:]:
        i = row.split(',')
             
        id_num = i[0]
        lon = float(i[3])
        lat = float(i[4].replace('\n', ""))

        charge_dict[id_num] = (lon, lat)

    return charge_dict


def extract_data():
    client = pymongo.MongoClient("localhost")
    db=client["full_houston"]

    print db.collection_names()
    return db.houston.find()



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
                self.radius_dct = {}

                self.property_codes = load_json(datadir + '/property_types_json/building_to_types.json')

                self.prop_vals = set(self.property_codes.values())
                self.missed_types=[]    
                self.charging_stations = charging_stations

                self.radius_maker()
                

        def buffer_point(self, point):
            buffer = point.buffer(self.radius_size)
            blocks = buffer
            return blocks

        def count_in_buffer(self):

            for station in self.charging_stations.keys()[1:2]:

                print station

                a,b =  self.charging_stations[station]

                #x_min, x_max = x - self.radius_size + x, self.rad

                #point = Point(x, y)
            
                #buffered_point = self.buffer_point(point)




                

                self.dct[station] =  dict([ ("num_" + p.lower(),  []) for p in self.prop_vals])

                for feature in self.features[1:1000]:

                    x,y = feature['geometry']['coordinates']

                    if ((x-a)**2 + (y-b)**2) <= self.radius_size**2:
                        #print "inside Loop"
                        try: 
                            #print "try"
                            bt = feature['properties']['BT']
                            prop_type = self.property_codes[bt]
                            #print bt, prop_type, '\n'
                            for p_val in self.prop_vals:
                                #if p_val == prop_type:
                                    #print p_val, prop_type
                                self.add_types(feature, station, prop_type, desc=p_val, dict_location="num_" + p_val.lower())



                        except KeyError as e:
                            #print "error"
                            self.missed_types.append(bt)
                            
            


        def add_types(self, feature, hash_location, prop_type, desc, dict_location): 
            """
            This checks to see if the property type matches the specified type

                Note:
                  called in the method check_grid. 

                Args:
          feature, 
          hash_location
          prop_type
          desc
          dict_location
            """
            #print "prop_type == desc",prop_type == desc

            if prop_type == desc:
                #print feature['properties']['HCAD_NUM']
                self.dct[hash_location][dict_location].append(feature['properties']['HCAD_NUM'])


        def calculate_values(self):

            for key, value in sorted(self.dct.iteritems()):
                for p_val in self.prop_vals:
                    self.radius_dct[key] = dict([ ("tot_num_" + p_val.lower(),  len(value[ "num_" + p_val.lower()])) for p_val in self.prop_vals])

        def write_to_file(self):
            f = open(self.charging_stations, 'r')

            data = f.readlines()


            for row in data[1:]:
                i = row.split(',')
                id_num = i[1]
                time = i[2]
                usage = i[3]

                lat = i[4]
                lon = i[5]

                indep_vas = self.radius_dct[id_num].values()

                independent = ','.join(str(e) for e in indep_vas)


                f.write(id_num + "," + str(usage) + "," + str(time)  + ","+ str(lon)  + "," + str(lat) + "," + independent + '\n')

            f.close()

        def radius_maker(self):

            self.count_in_buffer()
            self.calculate_values()
            self.write_to_file()



def main(sys_args):
        parser = _build_parser(sys_args[0])
        args = parser.parse_args(sys_args[1:])

        radius_size = args.radius_size
        county_name = args.county_name
        features = extract_data()

        charging_stations = join(datadir, 'charging_stations', render_file_style(county_name), 'prep.csv')

        if exists(charging_stations):
            charging_stations = make_charging_station_dict(charging_stations)

            r = RadiusMaker(radius_size, county_name, features, charging_stations)



        print('Done.')  







if __name__ == '__main__':
    sys.exit(main(sys.argv))