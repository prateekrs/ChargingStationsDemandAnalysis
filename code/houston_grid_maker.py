import argparse
import textwrap
import sys, os
import json

import numpy as np



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

    parser.add_argument(
            '--json_file',
            required=True,
            type=str,
            help= 'location of json file')

    return parser

def get_directories(path):
    cwd = os.path.dirname(os.path.abspath(__file__))
    dir_location = os.path.join(os.path.split(cwd)[0], path)
    return dir_location


def make_grid(grid_size, features):
	tot_minx=float("inf")
	tot_miny=float("inf")
	tot_maxx=0.0
	tot_maxy=0.0
	

	for num in range(len(features)):
		x, y = features[num]['geometry']["coordinates"]

		if x < tot_minx:
			tot_minx = x

		if y < tot_miny:
			tot_miny = y

		if x > tot_maxx:
			tot_maxx = x

		if y > tot_maxy:
			tot_maxy = y

	xgrid = np.arange(tot_minx, tot_maxx, grid_size)
	ygrid = np.arange(tot_miny, tot_maxy, grid_size)

	return xgrid, ygrid


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
		self.dct = {}
		self.grid_dct = {}
		

	def check_grid(self):
		for num in range(len(self.features)):
			x, y = self.features[num]['geometry']["coordinates"]
			ix = np.searchsorted(self.xgrid, x)
			iy = np.searchsorted(self.ygrid, y)
			hash_location = 'x' + str(ix) +'_y'+ str(iy)

			if hash_location not in self.dct:
				self.dct[hash_location] = {'num_buildings':[], 'num_condos': []}

			self.dct[hash_location]['num_buildings'].append(self.features[num]['properties']['HCAD_NUM'])

			
			if self.features[num]['properties']['CONDO_FLAG'] == "1":
				self.dct[hash_location]['num_condos'].append(self.features[num]['properties']['HCAD_NUM'])

	def calculate_grid(self):
		for key, value in sorted(self.dct.iteritems()):
			num_buildings = len(value['num_buildings'])
			num_condos = len(value['num_condos'])

			self.grid_dct[key] = {'tot_num_buildings': num_buildings, 'tot_num_condos': num_condos}


	def adjust_grid(self):
		possible_grids = make_possible_grids(self.xgrid, self.ygrid)
		for key in possible_grids:
			if key not in self.grid_dct.keys():
				self.grid_dct[key] = {'tot_num_buildings': -9999, 'tot_num_condos': -9999}

	def raster_maker(self):

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
	features = json.load(open(args.json_file, 'r'))

	# features = json.load(open('/Users/mattstringer/research/Houston_analysis/houston.json', 'r'))

	grid = GridMaker(square_size, county_name, features)
	grid.check_grid()
	grid.calculate_grid()
	grid.adjust_grid()
	grid.raster_maker()


	print('Done.')	




if __name__ == '__main__':
	sys.exit(main(sys.argv))
	