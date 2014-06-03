
import sys, os

from shapely.geometry import shape, Point, MultiPoint, LineString
import matplotlib.pyplot as plt

from squaremaker import make_study_area_map, set_datum, plot_polygon, make_county_map
from database import query
from filemanage import *

from collections import defaultdict

import numpy as np
from pyproj import Proj, transform
import math

from pandas import DataFrame, Series
import pandas as pd

import argparse
import textwrap
from math import modf, floor

datadir, resultsdir = get_directories()

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




def make_possible_grids(xgrid, ygrid):

	possible_grids = []

	for x in range(len(xgrid)):
		for y in range(len(ygrid)):
			hash_location = 'x' + str(x+1) +'_y'+ str(y+1)
			possible_grids.append(hash_location)

	return possible_grids

def find_median(list_used):
	if len(list_used) > 3:
		return np.median(list_used)
	else:
		return -9999


def make_coverage(query_results, installers, xgrid, ygrid):
	dct = {}

	cap = Proj('+datum=NAD83 +lat_0=32.10 +lat_1=33.53 '
        '+lat_2=32.47 +lon_0=-116.15 +no_defs +proj=lcc +units=us-ft '
        '+x_0=2000000 +y_0=500000', preserve_units=True)


	wgs84 = Proj(init='epsg:4326')
	count = 0

	possible_grids = make_possible_grids(xgrid, ygrid)

	hashes = []
	dates = []
	installers = []



	for i in query_results:
		try:
			lat, lon, installer, date_installed = i[1], i[2], i[0], i[3]
			x, y = transform(wgs84, cap, lon, lat)
			ix = np.searchsorted(xgrid, x)
			iy = np.searchsorted(ygrid, y)
			hash_location = 'x' + str(ix) +'_y'+ str(iy)
			# f1.write(hash_location + ";"+ str(date_installed) + ";" + str(installer) + '\n')

			hashes.append(hash_location)
		
			if (date_installed is None):
				dates.append('None')
				installers.append('None')

			else:
				dates.append(date_installed.year)
				installers.append(installer)



		except Exception as e:
			print(e)

	f1 = open('san_francisco.csv', 'w')
	print len(hashes), len(installers), len(dates)
	d = {'year': dates, 'installer': installers, 'location': hashes}
	df = DataFrame(data=d)




	for hash_local, group1 in df.groupby(['location'], sort=True):
		f1.write(hash_local + ",")


		num_buildings = len(group1)
		num_install_total = 0

		for year, group2 in group1.groupby(['year'], sort=True):
			if year != 'None':
				num_installs = len(group2)
				num_install_total += num_installs

				market_penetration = float(num_install_total) / float(num_buildings) 
				print hash_local, year, market_penetration, num_buildings



			# if date_installed != None:
			# 	year = str(date_installed.year)
			# 	if year not in dct:
			# 		dct[year] = 1
			# 		for grid in possible_grids:
			# 			dct[year] = {grid: {'num_buildings':1, 'total_num_adopters': 1, 'building_ages': 1, 'building_size': 1}}

			# 	else:

			# 		dct[year][grid] = {'num_buildings':1, 'total_num_adopters': 1, 'building_ages': 1, 'building_size': 1}





	f1.close()

		# 

	# 	try:
	# 		


	# 		if i[4] != None:
	# 			count += 1
	# 			if (count % 1000) == 0:
	# 				print count  



	# 			if hash_location not in dct:
	# 				dct[hash_location] = {'num_buildings':[], 'total_num_adopters': [], 'building_ages': [], 'building_size': []}

	# 				for installer in installers:
	# 					dct[hash_location][installer] = {'total_num_adopters': []}


	# 			dct[hash_location]['num_buildings'].append(i[4])

	# 			# if int(i[7]) > 0:
	# 			if i[7] != None:
	# 				dct[hash_location]['building_ages'].append(int(i[7]))

	# 				dct[hash_location]['building_size'].append(int(i[4]))


	# 			if i[0] in installers:
	# 				dct[hash_location][i[0]]['total_num_adopters'].append(i[4])

	# 			# check for installations
	# 			if i[0] not in [None, 'null']:
	# 				dct[hash_location]['total_num_adopters'].append(i[4])

	# 	except Exception as e:
	# 		print(e)

	# 	grid_dict = {}

	# 	for key, value in sorted(dct.iteritems()):
	# 		num_buildings = len(value['num_buildings'])
	# 		num_adopters = len(value['total_num_adopters'])
	# 		try:
	# 			market_share =  float(num_adopters) / float(num_buildings)
	# 		except Exception as e:
	# 			market_share = 0.0

	# 		grid_dict[key] = {'tot_num_buildings': num_buildings, 
	# 					'median_value_building': find_median(value['num_buildings']),
	# 					'num_addopters': len(value['total_num_adopters']),
	# 					'adopters_median_value': find_median(value['total_num_adopters']),
	# 					'home_age_median': find_median(value['building_ages']),
	# 					'building_size_median': find_median(value['building_size'])}
			 

	# possible_grids = make_possible_grids(xgrid, ygrid)

	# for key in possible_grids:
	# 	if key not in grid_dict.keys():
	# 		grid_dict[key] = {'tot_num_buildings': -9999,
	# 				'num_addopters': -9999, 
	# 				'median_value_building': -9999,
	# 				'adopters_median_value': -9999,
	# 				'home_age_median': -9999,
	# 				'building_size_median': -9999}

	# return grid_dict
	return dct


def color_grid(grid_dict, item):

	values = []

	for box in grid_dict:
		value = grid_dict[box][item]
		if value != -9999:
			values.append(value)


	percentile_25 = np.percentile(values, 25) # return 25th percentile, e.g median.
	percentile_50 = np.percentile(values, 50) # return 5th percentile, e.g median.		
	percentile_75 = np.percentile(values, 75) # return 25th percentile, e.g median.
	max_value = max(values) + 1000				

	return percentile_25, percentile_50, percentile_75, max_value



def find_color(value, percentiles):

	colors = ['#ffffd4', '#fed98e', '#fe9929']

	if value == -9999:
		color = 'w'

	else:
		count = 0	
		for i in percentiles:
			if value >= i:
				color = colors[count]
						
			else:
				color = colors[count]
				break

			count += 1

	return color

def numpy_grid(xgrid, ygrid, county_name):

	file_county = render_file_style(county_name)
	aggr_json = datadir + '/json_files/coverage_files/' + file_county + "_aggr[size-" + str(square_size) + "].json"

	grid_dict = load_json(aggr_json)

	coverage_files_dir = datadir + '/environment_coverage/' + file_county

	for item in grid_dict[grid_dict.keys()[0]]:
		fig = plt.figure()
		fig.add_subplot(111, aspect='equal')
		plt.title(item)
		ax = fig.gca()
		print('making grid ' + item)
		
		geometry, geo_limit = make_county_map(county_name, geobounds=False, color='#787878')
		plot_polygon(ax, geometry, color='w')

		percentiles = color_grid(grid_dict, item)
		# need to check if everything is save appropriately, i.e. x, y in grid in right spot.

		grid = []

		for y in reversed(range(len(ygrid))):
			row = [] 
			for x in range(len(xgrid)):
				value = grid_dict['x'+str(x+1) +'_y'+str(y+1)][item]
				row.append(value)

				x1, y1 = xgrid[x], ygrid[y]
				square_coors = [(x1, y1), (x1+10000, y1), (x1+10000, y1+10000), (x1, y1+10000)]
				sqared_geom = {"type": "Polygon", "coordinates": [square_coors]}
				geometry = shape(sqared_geom)

				try:
					color = find_color(value, percentiles)
				except Exception as e:
					color = 'w'
				
				plot_polygon(ax, geometry, color=color)

			grid.append(row)

		grid_array = np.array(grid)

		# plt.show()
		plt.savefig(resultsdir + '/maps/grid_maps/' + file_county + '/' +  item + "-coverage_raster.png", bbox_inches='tight') 

		print len(xgrid), grid_array.shape[1]
		print len(ygrid), grid_array.shape[0]
		assert(len(xgrid) == grid_array.shape[1])
		assert(len(ygrid) == grid_array.shape[0])

		assert xgrid[-1] > xgrid[0]
		assert ygrid[-1] > ygrid[0]


		header =  "ncols     %s\n" % grid_array.shape[1]
		header += "nrows    %s\n" % grid_array.shape[0]
		header += "xllcorner %s\n" % xgrid[0]
		header += "yllcorner %s\n" % ygrid[0]
		header += "cellsize %s\n" % square_size
		header += "NODATA_value -9999"

		coverage_file = coverage_files_dir +"/" +item + ".asc"
		np.savetxt(coverage_file, grid_array, header=header, fmt="%1.2f", comments='')
		print('Saved grid.')

def main(sys_args):

	parser = _build_parser(sys_args[0])
	args = parser.parse_args(sys_args[1:])

	county_name = args.county_name

	square_size = float(args.square_size)

	print('Started writing files')



	### stuff to use 
	xgrid, ygrid, geometry1 = make_study_area_map(county_name, square_size)


	installers = load_json(datadir + '/companies/companies_by_county.json')[county_name].keys()
	num_installers = len(installers)
	query_results = query(county_name)
	# # grid_dict = make_dict(query_results, installers, xgrid, ygrid)
	# # grid_dict = make_annual_dict(query_results, installers, xgrid, ygrid)
	grid_dict = make_coverage(query_results, installers, xgrid, ygrid)
	file_county = render_file_style(county_name)

	aggr_json = datadir + '/json_files/coverage_files/' + file_county + "_aggr[size-" + str(square_size) + "].json"

	# make_directory(coverage_files_dir)
	write_json(aggr_json, grid_dict)

	# numpy_grid(xgrid, ygrid, county_name)
	
	

	
	J = JSD()


if __name__ == '__main__':

    sys.exit(main(sys.argv))
    print('Done.')
