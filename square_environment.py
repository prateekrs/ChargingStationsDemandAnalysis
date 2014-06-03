import sys, os

from squaremaker import make_study_area_map, set_datum
from database import query
from filemanage import load_json, write_json, get_directories

from collections import defaultdict

import numpy as np
from pyproj import Proj, transform
import math



class JSD(object):
    def __init__(self):
        self.log2 = math.log(2)


    def KL_divergence(self, p, q):
        """ Compute KL divergence of two vectors, K(p || q)."""
        return sum(_p * math.log(_p / _q) for _p, _q in zip(p, q) if _p != 0)

    def Jensen_Shannon_divergence(self, p, q):
        """ Returns the Jensen-Shannon divergence. """
        self.JSD = 0.0
        weight = 0.5
        average = np.zeros(len(p)) #Average
        
        for x in range(len(p)):
            average[x] = weight * p[x] + (1 - weight) * q[x]
            self.JSD = (weight * self.KL_divergence(np.array(p), average)) + ((1 - weight) * self.KL_divergence(np.array(q), average))
        
        return self.JSD / self.log2


def make_possible_grids(xgrid, ygrid):

	possible_grids = []

	for x in range(len(xgrid)):
		for y in range(len(ygrid)):
			hash_location = 'x' + str(x+1) +'_y'+ str(y+1)
			possible_grids.append(hash_location)

	return possible_grids

def find_median(list_used):
	if len(list_used) > 0:
		return np.median(list_used)
	else:
		return -9999


def make_coverage(query_results, installers, xgrid, ygrid):
	dct = {}





	cap = Proj('+datum=NAD83 +lat_0=32.10 +lat_1=33.53 '
        '+lat_2=32.47 +lon_0=-116.15 +no_defs +proj=lcc +units=us-ft '
        '+x_0=2000000 +y_0=500000', preserve_units=True)


	wgs84 = Proj(init='epsg:4326')

	for i in query_results:
		lat, lon = i[1], i[2]
		x, y = transform(wgs84, cap, lon, lat)

		ix = np.searchsorted(xgrid, x)
		iy = np.searchsorted(ygrid, y)

		hash_location = 'x' + str(ix) +'_y'+ str(iy)

		if hash_location not in dct:
			dct[hash_location] = {'num_buildings':[], 'total_num_adopters': [], 'building_ages': [], 'building_size': []}

			for installer in installers:
				dct[hash_location][installer] = {'total_num_adopters': []}


		dct[hash_location]['num_buildings'].append(i[4])

		if int(i[7]) > 0:
			dct[hash_location]['building_ages'].append(int(i[7]))

			dct[hash_location]['building_size'].append(int(i[4]))


		if i[0] in installers:
			dct[hash_location][i[0]]['total_num_adopters'].append(i[4])

		# check for installations
		if i[0] not in [None, 'null']:
			dct[hash_location]['total_num_adopters'].append(i[4])

	grid_dict = {}

	for key, value in sorted(dct.iteritems()):
		num_buildings = len(value['num_buildings'])
		num_adopters = len(value['total_num_adopters'])
		try:
			market_share =  float(num_adopters) / float(num_buildings)
		except Exception as e:
			market_share = 0.0

		grid_dict[key] = {'tot_num_buildings': num_buildings, 
					'median_value_building': find_median(value['num_buildings']) * 1000,
					'num_addopters': len(value['total_num_adopters']),
					'adopters_median_value': find_median(value['total_num_adopters']) * 1000,
					'home_age_median': find_median(value['building_ages']),
					'building_size_median': find_median(value['building_size'])}
		 

	possible_grids = make_possible_grids(xgrid, ygrid)

	for key in possible_grids:
		if key not in grid_dict.keys():
			grid_dict[key] = {'tot_num_buildings': -9999,
					'num_addopters': -9999, 
					'median_value_building': -9999,
					'adopters_median_value': -9999,
					'home_age_median': -9999,
					'building_size_median': -9999}

	return grid_dict


# def make_dict(query_results, installers, xgrid, ygrid):
# 	dct = {}


# 	cap = Proj('+datum=NAD83 +lat_0=32.10 +lat_1=33.53 '
#         '+lat_2=32.47 +lon_0=-116.15 +no_defs +proj=lcc +units=us-ft '
#         '+x_0=2000000 +y_0=500000', preserve_units=True)


# 	wgs84 = Proj(init='epsg:4326')

# 	for i in query_results:
# 		lat, lon = i[1], i[2]
# 		x, y = transform(wgs84, cap, lon, lat)

# 		ix = np.searchsorted(xgrid, x)
# 		iy = np.searchsorted(ygrid, y)

# 		hash_location = 'x' + str(ix) +'_y'+ str(iy)

# 		if hash_location not in dct:
# 			dct[hash_location] = {'num_buildings':[], 'total_num_adopters': []}

# 			for installer in installers:
# 				dct[hash_location][installer] = {'total_num_adopters': []}


# 		dct[hash_location]['num_buildings'].append(i[4])

# 		if i[0] in installers:
# 			dct[hash_location][i[0]]['total_num_adopters'].append(i[4])

# 		# check for installations
# 		if i[0] not in [None, 'null']:
# 			dct[hash_location]['total_num_adopters'].append(i[4])

# 	grid_dict = {}

# 	for key, value in sorted(dct.iteritems()):
# 		num_buildings = len(value['num_buildings'])
# 		num_adopters = len(value['total_num_adopters'])
# 		try:
# 			market_share =  float(num_adopters) / float(num_buildings)
# 		except Exception as e:
# 			market_share = 0.0

# 		grid_dict[key] = {'tot_num_buildings': num_buildings, 
# 					'median_value_building': np.median(value['num_buildings']) * 1000,
# 					'total_num_adopters': num_adopters,
# 					'total_market_penetration': market_share,
# 					'adopters_median_value': np.median(value['total_num_adopters']) * 1000,
# 					'installers': []
# 					}
		 
# 		for installer in installers:
# 			num_installations = len(value[installer]['total_num_adopters'])
# 			try:
# 				per_market = float(num_installations) / float(num_adopters)
# 			except ZeroDivisionError:
# 				per_market = 0.0

# 			grid_dict[key]['installers'].append({ installer: 
# 												{'total_num_adopters': num_installations,
# 												'per_market': per_market,
# 												'excessing_market': True}})

# 	return grid_dict

# def make_annual_dict(query_results, installers, xgrid, ygrid):

# 	dct = {}


# 	cap = Proj('+datum=NAD83 +lat_0=32.10 +lat_1=33.53 '
#         '+lat_2=32.47 +lon_0=-116.15 +no_defs +proj=lcc +units=us-ft '
#         '+x_0=2000000 +y_0=500000', preserve_units=True)


# 	wgs84 = Proj(init='epsg:4326')

# 	for i in query_results:
# 		lat, lon = i[1], i[2]
# 		x, y = transform(wgs84, cap, lon, lat)

# 		ix = np.searchsorted(xgrid, x)
# 		iy = np.searchsorted(ygrid, y)

# 		hash_location = 'x' + str(ix) +'_y'+ str(iy)

# 		if i[3] != None:

# 			year = i[3].year

# 			if year not in dct:

# 				dct[year] = {'square_results': []}

# 				if hash_location not in dct[year]['square_results']:

# 					dct[year]['square_results'].append({hash_location: 1})

# 				# for installer in installers:
# 	 		# 		dct[hash_location][installer] = {'total_num_adopters': []}





# 			# dct[year]['square_results'].append({'tot_num_buildings': 1, 
#  		# 			'median_value_building': 1,
#  		# 			'total_num_adopters': 1,
#  		# 			'total_market_penetration': 1,
#  		# 			'adopters_median_value': 1,
#  		# 			'installers': []})


# 	return dct


def main(county_name, square_size):

	datadir, resultsdir = get_directories()

	xgrid, ygrid, geometry = make_study_area_map(county_name, square_size)

	installers = load_json(datadir + '/companies/companies_by_county.json')

	# installers = installers[county_name].keys()
	# num_installers = len(installers)
	# query_results = query(county_name)
	# grid_dict = make_dict(query_results, installers, xgrid, ygrid)
	# grid_dict = make_annual_dict(query_results, installers, xgrid, ygrid)
	

	# grid_dict = make_coverage(query_results, installers, xgrid, ygrid)

	aggr_json = datadir + '/json_files/coverage_files/' + render_file_style(county_name) + "_aggr[size-" + str(square_size) + "].json"
	# write_json(aggr_json, grid_dict)

	grid_dict = load_json(aggr_json)

	for i in sorted(grid_dict):
		print i

	
	J = JSD()




	# for key, value in  grid_dict.iteritems():
	# 	print key, value



if __name__ == '__main__':
    county_name = 'San Francisco'
    square_size = 10000

    main(county_name, square_size)







