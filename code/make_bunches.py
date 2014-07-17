
import sys, os
from io import BytesIO
from os import makedirs
from os.path import join
from os.path import exists

import glob

from pyproj import Proj, transform

import numpy as np



from sklearn.datasets.base import get_data_home, Bunch
from sklearn.externals import joblib

sys.path.append('my_libraries')
from database import query
from filemanage import render_file_style, get_directories



cap = Proj('+datum=NAD83 +lat_0=27.50 +lat_1=30.17 '
    '+lat_2=28.23 +lon_0=-99.0 +no_defs +proj=lcc +units=us-ft '
    '+x_0=600000 +y_0=4000000', preserve_units=True)

wgs84 = Proj(init='epsg:4326')

datadir, resultsdir=get_directories()




def _load_coverage(F, header_length=7, dtype=np.int16):
    """
    load a coverage file.
    This will return a numpy array of the given dtype
    """
    try:
        header = [F.readline() for i in range(header_length)]

    except:
        F = open(F)
        header = [F.readline() for i in range(header_length)]

    headers = {}

    for i, t in enumerate(header):
        item = t.split()[0]
        var = t.split()[1]


        if i == 0:
            var = str(var)
        else:
            var = float(var)

        headers[item] = var
    
    M = np.loadtxt(F, dtype=dtype)
    nodata = headers['NODATA_value']
    if nodata != -9999:
        M[nodata] = -9999
    return M, headers

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




    rec = np.loadtxt(F, skiprows=1, delimiter=',', dtype='a22,i4,i4,f4,f4')
    rec.dtype.names = names



    return rec

def make_test_train_split(file_location):
#

	f1 = open(file_location + '/prep.csv', 'w')
	f1.write("id_num,usage,time,x,y\n")


	prep = []


	f = open(file_location + "/DC_charging_stations_MonthlyDemand.csv", 'r')
	data = f.readlines()


	locations = []



        for row in data[1:]:
            i = row.split(',')
            id_num = i[1]
            time = i[2]
            usage = i[3]

            lat = i[4]
            lon = i[5]
            
            locations.append(id_num)

            x, y = transform(wgs84, cap, lon, lat)
            tuple_items = (id_num, time, usage, x, y)
            prep.append(tuple_items)
            f1.write(id_num + "," + str(usage) + "," + str(time)  + "," + str(x) + ","+ str(y) + '\n')


	f1.close()


	locations = list(set(locations))
	return locations




def fetch_installer_distributions(county_name, data_home=None):
    """
    Loads data to make bunches

    Returns
    --------
    bunch (bunch object)


    """
	# make into a complete if else statement
    DATA_ARCHIVE_NAME = county_name + "_data_coverage.pkz"

    datadir, resultsdir = get_directories()

    if not exists(join(datadir, 'bunches', DATA_ARCHIVE_NAME)):
        file_location = datadir + '/charging_stations/' + render_file_style(county_name) 

        locations = make_test_train_split(file_location)
        prep = _load_csv(file_location + '/prep.csv')

        file_county = render_file_style(county_name)
        coverage_files_dir = datadir + '/raster_files/' + file_county + "/*.asc"

        dtype = np.int16

        coverages = []
        header = None
        features = []

        for f in glob.glob(coverage_files_dir):
            cov, header = _load_coverage(f)
            coverages.append(cov)
            features.append(header['feature'])


        coverages = np.asarray(coverages, dtype=dtype)

        extra_params = dict(x_left_lower_corner=header['xllcorner'],
	                        Nx=header['ncols'],
	                        y_left_lower_corner=header['yllcorner'],
	                        Ny=header['nrows'],
	                        grid_size=header['cellsize'])

        bunch = Bunch(coverages=coverages, stations=prep, locations=locations, features=features, **extra_params)
        joblib.dump(bunch, join(datadir, 'bunches', DATA_ARCHIVE_NAME), compress=9)
        bunch = joblib.load(join(datadir, 'bunches', DATA_ARCHIVE_NAME))
        return bunch

    else:

		bunch = joblib.load(join(datadir, 'bunches', DATA_ARCHIVE_NAME))
		return bunch
	





if __name__ == '__main__':
	county_name = 'harris'

	fetch_installer_distributions(county_name)
