from __future__ import print_function
import argparse
import textwrap


from time import time
import os

import numpy as np
# import pylab as pl
import matplotlib.pyplot as plt

# pl.rcParams['figure.figsize'] = 20, 5

from make_bunches import fetch_installer_distributions, construct_grids
from sklearn.datasets.base import Bunch
from sklearn import svm, metrics
from database import Database
import json
sys.path.append('my_libraries')
import random
from squaremaker import make_study_area_map, make_county_map, plot_polygon,construct_grids

from filemanage import serialize_object
from pyproj import Proj, transform


# if basemap is available, we'll use it.
# otherwise, we'll improvise later...
try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False



cwd = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(os.path.split(cwd)[0], 'data')
resultsdir = os.path.join(os.path.split(cwd)[0], 'results')


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



    
def create_bunch(stations, coverages, xgrid, ygrid, independent_vars):
    """
    create a bunch with information about a particular organism

    This will use the test/train record arrays to extract the
    data specific to the given species name.
    """

     


    points = dict(stations=stations)

    i_title = ','.join(str(e) for e in independent_vars)


    f1 = open(datadir + '/regression/regression_file.csv', 'w')
    f1.write("id_num,time,usage," + i_title + "\n")

    for label, pts in points.iteritems():


        # choose points that fall with study area
        pts = pts[pts['x'] > min(xgrid)]
        pts = pts[pts['x'] < max(xgrid)]
        pts = pts[pts['y'] > min(ygrid)]
        pts = pts[pts['y'] < max(ygrid)]

        ix = np.searchsorted(xgrid, pts['x'])
        iy = np.searchsorted(ygrid, pts['y'])

        time = pts['time']
        id_num = pts['id_num']
        usage = pts['usage']

        c_f = coverages[:, -iy, ix].T.tolist()



        strs= ''.join(str(e) for e in c_f)

        for item in zip(time, id_num, usage, c_f):
            independent = ','.join(str(e) for e in item[3])

            f1.write(str(item[1])  + ',' + str(item[0])  + ',' + str(item[2]) + "," +  independent + "\n")

    f1.close()





def main(county_name, square_size):

    data = fetch_installer_distributions(county_name)

    # Set up the data grid
    xgrid, ygrid = construct_grids(data)
    X, Y = np.meshgrid(xgrid, ygrid[::-1])

    independent_vars = data.features

    charging_stations = data.locations
    num_stations = len(charging_stations)

    create_bunch(data.stations, data.coverages, xgrid, ygrid, independent_vars)





if __name__ == '__main__':
    county_name = 'harris'
    square_size = 10000
    main(county_name, square_size)

