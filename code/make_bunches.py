
import sys, os
from io import BytesIO
from os import makedirs
from os.path import join
from os.path import exists

import glob

import random
from pyproj import Proj, transform

import numpy as np



from sklearn.datasets.base import get_data_home, Bunch
from sklearn.externals import joblib

sys.path.append('my_libraries')
from database import query
from filemanage import render_file_style



cap = Proj('+datum=NAD83 +lat_0=27.50 +lat_1=30.17 '
    '+lat_2=28.23 +lon_0=-99.0 +no_defs +proj=lcc +units=us-ft '
    '+x_0=600000 +y_0=4000000', preserve_units=True)

wgs84 = Proj(init='epsg:4326')


def get_directories():
    cwd = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(os.path.split(cwd)[0], 'data')
    resultsdir = os.path.join(os.path.split(cwd)[0], 'results')
    return datadir, resultsdir

def construct_grids(batch):
    """Construct the map grid from the batch object

    Parameters
    ----------
    batch : Batch object
        The object returned by :func:`fetch_species_distributions`

    Returns
    -------
    (xgrid, ygrid) : 1-D arrays
        The grid corresponding to the values in batch.coverages
    """
    # x,y coordinates for corner cells
    xmin = batch.x_left_lower_corner + batch.grid_size
    xmax = xmin + (batch.Nx * batch.grid_size)
    ymin = batch.y_left_lower_corner + batch.grid_size
    ymax = ymin + (batch.Ny * batch.grid_size)

    # x coordinates of the grid cells
    xgrid = np.arange(xmin, xmax, batch.grid_size)
    # y coordinates of the grid cells
    ygrid = np.arange(ymin, ymax, batch.grid_size)

    return (xgrid, ygrid)


def _load_coverage(F, header_length=6, dtype=np.int16):
    """
    load a coverage file.
    This will return a numpy array of the given dtype
    """
    try:
        header = [F.readline() for i in range(header_length)]
    except:
        F = open(F)
        header = [F.readline() for i in range(header_length)]


    make_tuple = lambda t: (t.split()[0], float(t.split()[1]))
    header = dict([make_tuple(line) for line in header])

    M = np.loadtxt(F, dtype=dtype)
    nodata = header['NODATA_value']
    if nodata != -9999:
        M[nodata] = -9999
    return M, header

def _load_csv(F):
    """Load csv file.

    Parameters
    ----------
    F : string or file object
        file object or name of file

    Returns
    -------
    rec : np.ndarray
        record array representing the data
    """
    try:
        names = F.readline().strip().split(',')
    except:
        F = open(F)
        names = F.readline().strip().split(',')

    rec = np.loadtxt(F, skiprows=1, delimiter=',',
                     dtype='a22,f4,f4')
    rec.dtype.names = names

    return rec

def make_test_train_split(file_location):

	if os.path.isfile(file_location + '/train.csv') == False:
		print('writing training sets')
		print file_location + '/train.csv'


		f1 = open(file_location + '/train.csv', 'w')
		f1.write("location,x,y\n")
		f2 = open(file_location + '/test.csv', 'w')
		f2.write("location,x,y\n")

		train = []
		test = []

		f = open(file_location + "/charging_stations_lat-lon.csv", 'r')
		data = f.readlines()
		print "yeps"



		for row in data:

			row = row.split('\r')
			for items in row[1:]:

				i = items.split(',')

				location = i[0]
				lat = i[1]
				lon = i[2]

				x, y = transform(wgs84, cap, lon, lat)
				tuple_items = (location, x,y)
				rand = random.random()

				if rand > 0.2:
					train.append(tuple_items)
					f1.write(location + "," + str(x) + ","+ str(y) + '\n')

	   			elif rand < 0.2:
					test.append(tuple_items)
					f2.write(location + "," + str(x) + ","+ str(y) + '\n')

		f1.close()
		f2.close()
		print  float(len(train)) / float(len(train) + len(test))
	
	else:
		print "test train sets written"


def fetch_installer_distributions(county_name, data_home=None):
	# make into a complete if else statement
	DATA_ARCHIVE_NAME = "data_coverage.pkz"

	datadir, resultsdir = get_directories()
	print datadir

	if not exists(join(datadir, 'bunches', DATA_ARCHIVE_NAME)):


		file_location = datadir + '/charging_stations/' + render_file_style(county_name) 

		make_test_train_split(file_location)

		train = _load_csv(file_location + '/train.csv')
		test = _load_csv(file_location + '/test.csv')

		file_county = render_file_style(county_name)
		coverage_files_dir = datadir + '/environment_coverage/' + file_county + "/*.asc"

		dtype = np.int16

		coverages = []
		header = None
		for f in glob.glob(coverage_files_dir):
			cov, header = _load_coverage(f)
			header = header
			coverages.append(cov)

		coverages = np.asarray(coverages, dtype=dtype)

		extra_params = dict(x_left_lower_corner=header['xllcorner'],
	                        Nx=header['ncols'],
	                        y_left_lower_corner=header['yllcorner'],
	                        Ny=header['nrows'],
	                        grid_size=header['cellsize'])

		bunch = Bunch(coverages=coverages, test=test, train=train, **extra_params)
		joblib.dump(bunch, join(datadir, 'bunches', DATA_ARCHIVE_NAME), compress=9)
		bunch = joblib.load(join(datadir, 'bunches', DATA_ARCHIVE_NAME))
		return bunch

	else:

		bunch = joblib.load(join(datadir, 'bunches', DATA_ARCHIVE_NAME))
		return bunch
	# joblib.dump(bunch, join(data_home, DATA_ARCHIVE_NAME), compress=9)





if __name__ == '__main__':
	county_name = 'harris'

	fetch_installer_distributions(county_name)
