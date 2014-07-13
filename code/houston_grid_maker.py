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
										   		'num_banks': [],
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
			 	self.add_types(feature, hash_location, prop_type, desc='Residential', dict_location='num_residential')
			 	self.add_types(feature, hash_location, prop_type, desc='Office', dict_location='num_offices')
			 	self.add_types(feature, hash_location, prop_type, desc='Industrial', dict_location='num_industrial')
			 	self.add_types(feature, hash_location, prop_type, desc='Warehouse', dict_location='num_warehouse')
			 	self.add_types(feature, hash_location, prop_type, desc='Restaurants', dict_location='num_offices')
			 	self.add_types(feature, hash_location, prop_type, desc='AmusementPark', dict_location='num_restaurant')
			 	self.add_types(feature, hash_location, prop_type, desc='Theatres', dict_location='num_theatres')
			 	self.add_types(feature, hash_location, prop_type, desc='Shopping', dict_location='num_shopping')
			 	self.add_types(feature, hash_location, prop_type, desc='Social', dict_location='num_social')
			 	self.add_types(feature, hash_location, prop_type, desc='Medical', dict_location='num_medical')
			 	self.add_types(feature, hash_location, prop_type, desc='Banks', dict_location='num_banks')
			 	self.add_types(feature, hash_location, prop_type, desc='Transport', dict_location='num_transport')
			 	self.add_types(feature, hash_location, prop_type, desc='Library', dict_location='num_library')
			 	self.add_types(feature, hash_location, prop_type, desc='PostOffice', dict_location='num_postoffice')
			 	self.add_types(feature, hash_location, prop_type, desc='EmergencyStation', dict_location='num_emergencystation')
			 	self.add_types(feature, hash_location, prop_type, desc='Correctional', dict_location='num_correctional')
			 	self.add_types(feature, hash_location, prop_type, desc='CarDealerships', dict_location='num_cardealership')
			 	self.add_types(feature, hash_location, prop_type, desc='GasCompany', dict_location='num_gascompany')
			 	self.add_types(feature, hash_location, prop_type, desc='ElectricCompany', dict_location='num_electriccompany')
			 	self.add_types(feature, hash_location, prop_type, desc='Railroad', dict_location='num_railroad')
			 	self.add_types(feature, hash_location, prop_type, desc='Pipeline', dict_location='num_pipeline')
			 	self.add_types(feature, hash_location, prop_type, desc='Telephone', dict_location='num_telephone')


			except KeyError as e:
				self.missed_types.append(bt)


			if feature['properties']['CONDO_FLAG'] == "1":
				self.dct[hash_location]['num_condos'].append(feature['properties']['HCAD_NUM'])


		print self.missed_types

	def add_types(self, feature, hash_location, prop_type, desc, dict_location):
		if prop_type == desc:
			self.dct[hash_location][dict_location].append(feature['properties']['HCAD_NUM'])


	def calculate_grid(self):
		for key, value in sorted(self.dct.iteritems()):
			num_buildings = len(value['num_buildings'])
			num_condos = len(value['num_condos'])
			num_residential = len(value['num_residential'])
			num_offices= len(value['num_offices'])
			num_industrial = len(value['num_industrial'])

			num_warehouse = len(value['num_warehouse'])
			num_restaurant = len(value['num_restaurant'])
			num_amusementpark = len(value['num_amusementpark'])
			num_recreation = len(value['num_recreation'])
			num_theatres = len(value['num_theatres'])
			num_banks = len(value['num_banks'])
			num_shopping = len(value['num_shopping'])
			num_medical = len(value['num_medical'])
			num_social = len(value['num_social'])
			num_transport = len(value['num_transport'])
			num_library = len(value['num_library'])
			num_postoffice = len(value['num_postoffice'])
			num_religious = len(value['num_religious'])
			num_emergencystation = len(value['num_emergencystation'])
			num_correctional = len(value['num_correctional'])
			num_cardealership = len(value['num_cardealership'])
			num_gascompany = len(value['num_gascompany'])
			num_electriccompany = len(value['num_electriccompany'])
			num_railroad = len(value['num_railroad'])
			num_pipeline = len(value['num_pipeline'])
			num_telephone = len(value['num_telephone'])


			


			self.grid_dct[key] = {'tot_num_buildings': num_buildings, 'tot_num_condos': num_condos, 'tot_num_residential': num_residential,'tot_num_offices':num_offices, 'tot_num_industrial': num_industrial, 'tot_num_warehouse': num_warehouse, 'tot_num_restaurant': num_restaurant,'tot_num_amusementpark': num_amusementpark, 'tot_num_recreation': num_recreation, 'tot_num_theatres': num_theatres,'tot_num_banks': num_banks, 'tot_num_shopping': num_shopping, 'tot_num_medical': num_medical, 'tot_num_social': num_social, 'tot_num_transport': num_transport, 'tot_num_library': num_library, 'tot_num_postoffice': num_postoffice, 'tot_num_religious': num_religious, 'tot_num_emergencystation': num_emergencystation, 'tot_num_correctional': num_correctional,'tot_num_cardealership':  num_cardealership,'tot_num_gascompany': num_gascompany, 'tot_num_electriccompany': num_electriccompany,'tot_num_railroad': num_railroad, 'tot_num_pipeline': num_pipeline,'tot_num_telephone': num_telephone}


	def adjust_grid(self):
		
		for key in self.possible_grids:
			if key not in self.grid_dct.keys():
				self.grid_dct[key] = {'tot_num_buildings': -9999, 'tot_num_condos': -9999, 'tot_num_residential': -9999, 'tot_num_offices':-9999, 'tot_num_industrial': -9999, 'tot_num_warehouse': -9999, 'tot_num_restaurant': -9999,'tot_num_amusementpark': -9999, 'tot_num_recreation': -9999, 'tot_num_theatres': -9999,'tot_num_banks': -9999, 'tot_num_shopping': -9999, 'tot_num_medical': -9999, 'tot_num_social': -9999, 'tot_num_transport': -9999, 'tot_num_library': -9999, 'tot_num_postoffice': -9999, 'tot_num_religious': -9999, 'tot_num_emergencystation': -9999, 'tot_num_correctional': -9999,'tot_num_cardealership':  -9999,'tot_num_gascompany': -9999, 'tot_num_electriccompany': -9999,'tot_num_railroad': -9999, 'tot_num_pipeline': -9999,'tot_num_telephone': -9999}

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
    

    return db.houston.find().limit(100000)

if __name__ == '__main__':
	sys.exit(main(sys.argv))
	
