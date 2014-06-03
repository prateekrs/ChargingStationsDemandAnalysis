from io import BytesIO
from os import makedirs
from os.path import join
from os.path import exists
from filemanage import *
import glob
from filemanage import *
import random
from pyproj import Proj, transform

import numpy as np

from database import query

from sklearn.datasets.base import get_data_home, Bunch
from sklearn.externals import joblib




cap = Proj('+datum=NAD83 +lat_0=32.10 +lat_1=33.53 '
    '+lat_2=32.47 +lon_0=-116.15 +no_defs +proj=lcc +units=us-ft '
    '+x_0=2000000 +y_0=500000', preserve_units=True)

wgs84 = Proj(init='epsg:4326')

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

def make_test_train_split(file_location, installers):

	if os.path.isfile(file_location + '/train.csv') == False:
		print('writing training sets')

		query_results = query(county_name)

		f1 = open(file_location + '/train.csv', 'w')
		f1.write("installer,x,y\n")
		f2 = open(file_location + '/test.csv', 'w')
		f2.write("installer,x,y\n")

		train = []
		test = []

		for i in query_results:
			if i[0] in installers:

				x, y = transform(wgs84, cap, i[2], i[1])
				tuple_items = (i[0], x,y)
				rand = random.random()

				if rand > 0.2:
					train.append(tuple_items)
					f1.write(i[0].replace(',', '').replace('  ', ' ') + "," + str(x) + ","+ str(y) + '\n')

	   			elif rand < 0.2:
					test.append(tuple_items)
					f2.write(i[0].replace(',', '').replace('  ', ' ') + "," + str(x) + ","+ str(y) + '\n')

		f1.close()
		f2.close()
		print  float(len(train)) / float(len(train) + len(test))
	
	else:
		print "test train sets written"


def fetch_installer_distributions(county_name, data_home=None):
	# make into a complete if else statement
	DATA_ARCHIVE_NAME = render_file_style(county_name)  + "_installation_coverage.pkz"

	datadir, resultsdir = get_directories()

	if not exists(join(datadir, 'bunches', DATA_ARCHIVE_NAME)):
		datadir, resultsdir = get_directories()


		installers = load_json(datadir + '/companies/companies_by_county.json')
		installers = installers[county_name].keys()

		file_location = datadir + '/installations/' + render_file_style(county_name)
		make_test_train_split(file_location, installers)

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
	county_name = 'San Diego'
	fetch_installer_distributions(county_name)
