import os, sys
#import geojson
from pyproj import Proj, transform
#from shapely.geometry import shape, Point, MultiPoint, LineString
import numpy as np

#from descartes.patch import PolygonPatch

import matplotlib.pyplot as plt





cap = Proj('+datum=NAD83 +lat_0=27.50 +lat_1=30.17 '
    '+lat_2=28.23 +lon_0=-99.0 +no_defs +proj=lcc +units=us-ft '
    '+x_0=600000 +y_0=4000000', preserve_units=True)

wgs84 = Proj(init='epsg:4326')






def main(file_location, file_write_location):
	f = open(file_location, 'r')
	data = f.readlines()


	f1 = open(file_write_location, 'w')

	f1.write("location,x,y\n")

	for row in data:
		row = row.split('\r')
		for items in row[1:]:

			i = items.split(',')
			location = i[0]
			lat = i[1]
			lon = i[2]
			x, y = transform(wgs84, cap, lon, lat)
			f1.write(location + "," + str(x) + "," + str(y) + "\n")
			
			


	f.close()
	f1.close()
	

if __name__ == '__main__':
	file_location = "/Users/mattstringer/research/Houston_analysis/data/charging_stations/charging_stations_lat-lon.csv"
	file_write_location = "/Users/mattstringer/research/Houston_analysis/data/charging_stations/charging_stations_feet-coordinates.csv"
	main(file_location, file_write_location)