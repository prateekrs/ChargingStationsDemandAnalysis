import argparse
import textwrap
import sys, os
import json
import numpy as np
import pymongo

# import addtional code from my_libraries
sys.path.append('my_libraries')
from squaremaker import make_grid
from filemanage import load_json

cwd = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(os.path.split(cwd)[0], 'data')
resultsdir = os.path.join(os.path.split(cwd)[0], 'results')



USAGE = textwrap.dedent("""\
	Create a dense data matrix from raw mixed features.""")

def _build_parser(prog):
    parser = argparse.ArgumentParser(prog=prog, description=USAGE)
    parser.add_argument(
            '--county_name',
            required=True,
            type=str,
            help='Name of county that you are currently matching, \n example is "San Diego"')

    parser.add_argument(
            '--square_size',
            required=True,
            type=int,
            help='county grid size - enter as an integer')

    return parser

def get_directories(path):
    cwd = os.path.dirname(os.path.abspath(__file__))
    dir_location = os.path.join(os.path.split(cwd)[0], path)
    return dir_location



def make_possible_grids(xgrid, ygrid):

	possible_grids = []

	for x in range(len(xgrid)):
		for y in range(len(ygrid)):
			hash_location = 'x' + str(x+1) +'_y'+ str(y+1)
			possible_grids.append(hash_location)

	return possible_grids


class GridMaker(object):

	def __init__(self, square_size, county_name, features):
		self.square_size = square_size
		self.county_name = county_name

		self.features = features

		self.xgrid, self.ygrid = make_grid(self.square_size, self.features)
		self.possible_grids = make_possible_grids(self.xgrid, self.ygrid)
		self.dct = {}
		self.grid_dct = {}

		self.property_codes = load_json(datadir + '/property_types_json/building_to_types.json')

		self.missed_types = []

		
		

	def check_grid(self):
		features = extract_data()
		for feature in features:
			
			x, y = feature['geometry']["coordinates"]
			ix = np.searchsorted(self.xgrid, x)
			iy = np.searchsorted(self.ygrid, y)
			hash_location = 'x' + str(ix) +'_y'+ str(iy)

			if hash_location not in self.dct:
				self.dct[hash_location] = 	{'num_buildings':[],
											'num_condos': [],

										   		'num_residential': [], 
										   		'num_offices': [], 
										   		'num_industrial': [], 
										   		'num_warehouse': [], 
										   		'num_restaurant': [],
										   		'num_amusementpark': [],
										   		'num_recreation': [],
										   		'num_theatres': [],
										   		'num_shopping': [], 
										   		'num_medical' : [],
										   		'num_social': [],
										   		'num_transport': [],
										   		'num_library': [],
										   		'num_postoffice':[],
										   		'num_religious': [],
										   		'num_emergencystation': [],
										   		'num_correctional': [],
										   		'num_cardealership': [],
										   		'num_gascompany': [],
										   		'num_electriccompany': [],
										   		'num_railroad': [],
										   		'num_pipeline':[],
										   		'num_telephone': []
										   		}

			self.dct[hash_location]['num_buildings'].append(feature['properties']['HCAD_NUM'])
			bt = feature['properties']['BT']

			try:
			 	prop_type = self.property_codes[bt]

			 	if prop_type == 'Residential':
			 		self.dct[hash_location]['num_residential'].append(feature['properties']['HCAD_NUM'])
			 	if prop_type == 'Office':
			 		self.dct[hash_location]['num_offices'].append(feature['properties']['HCAD_NUM'])

			except KeyError as e:
				self.missed_types.append(bt)


			if feature['properties']['CONDO_FLAG'] == "1":
				self.dct[hash_location]['num_condos'].append(feature['properties']['HCAD_NUM'])


		print self.missed_types

	def calculate_grid(self):
		for key, value in sorted(self.dct.iteritems()):
			num_buildings = len(value['num_buildings'])
			num_condos = len(value['num_condos'])
			num_residential = len(value['num_residential'])
			num_offices= len(value['num_offices'])


			self.grid_dct[key] = {'tot_num_buildings': num_buildings, 'tot_num_condos': num_condos, 'tot_num_residential': num_residential,'tot_num_offices':num_offices}


	def adjust_grid(self):
		
		for key in self.possible_grids:
			if key not in self.grid_dct.keys():
				self.grid_dct[key] = {'tot_num_buildings': -9999, 'tot_num_condos': -9999, 'tot_num_residential': -9999, 'tot_num_offices':-9999}

	def raster_maker(self):
		self.check_grid()
		self.calculate_grid()
		self.adjust_grid()
	

		for item in self.grid_dct[self.grid_dct.keys()[0]]:

			grid = []

			for y in reversed(range(len(self.ygrid))):
				row = []
				for x in range(len(self.xgrid)):
					value = self.grid_dct['x'+str(x+1) +'_y'+str(y+1)][item]
					row.append(value)

				grid.append(row)

			grid_array = np.array(grid)

			header =  "ncols     %s\n" % grid_array.shape[1]
			header += "nrows    %s\n" % grid_array.shape[0]
			header += "xllcorner %s\n" % self.xgrid[0]
			header += "yllcorner %s\n" % self.ygrid[0]
			header += "cellsize %s\n" % self.square_size
			header += "NODATA_value -9999"

			#remove hard coding.

			file_name = get_directories('data/raster_files/houston/') + item + ".asc"

			np.savetxt(file_name, grid_array, header=header, fmt="%1.2f", comments='')
			print('Saved grid.')


def main(sys_args):
	parser = _build_parser(sys_args[0])
	args = parser.parse_args(sys_args[1:])

	county_name = args.county_name
	square_size = float(args.square_size)

	features = extract_data()

	grid = GridMaker(square_size, county_name, features)
	grid.raster_maker()



	print('Done.')	

def extract_data():
    client = pymongo.MongoClient("localhost")
    db=client["houston_analysis_final1"]

    print db.collection_names()
    

    return db.houston.find().limit(10000)


if __name__ == '__main__':
	sys.exit(main(sys.argv))
	
