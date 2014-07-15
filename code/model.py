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
from filemanage import *
import random
from squaremaker import make_study_area_map, make_county_map, plot_polygon

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



    
def create_bunch(stations, coverages, xgrid, ygrid):
    """
    create a bunch with information about a particular organism

    This will use the test/train record arrays to extract the
    data specific to the given species name.
    """

     


    points = dict(stations=stations)

    f1 = open(datadir + '/regression/regression_file.csv', 'w')
    f1.write("id_num,usage,time,x,y\n")

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




        # for item in zip(time, id_num, usage, c_f[0], c_f[1], c_f[2], c_f[3], c_f[4], c_f[5], c_f[6], c_f[7], c_f[8], c_f[9], c_f[10], c_f[11], c_f[12], c_f[13], c_f[14], c_f[15], c_f[16], c_f[17], c_f[18], c_f[19], c_f[20], c_f[21], c_f[22], c_f[23], c_f[24], c_f[25], c_f[17]):
        for item in zip(time, id_num, usage, c_f):
            independent = ','.join(str(e) for e in item[3])

            f1.write(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + "," +  independent + "\n")

    f1.close()





def main(county_name, square_size):


    data = fetch_installer_distributions(county_name)

    # Set up the data grid
    xgrid, ygrid = construct_grids(data)
    X, Y = np.meshgrid(xgrid, ygrid[::-1])

    charging_stations = data.locations
    num_stations = len(charging_stations)
    # f, axarr = plt.subplots(2, num_stations, figsize=(22, 4))
    create_bunch(data.stations, data.coverages, xgrid, ygrid)





    np.random.seed(13)
    
    # background_points = np.c_[np.random.randint(low=0, high=data.Ny,
    #                                             size=10000),
    #                           np.random.randint(low=0, high=data.Nx,
    #                                             size=10000)].T


    # geometry, geo_limit = make_county_map(county_name)
    # Fit, predict, and plot for each species.
    # for i, installer in enumerate(bunches):
    #     # if i != 0:
    #     try:
    #         print("_" * 80)
    #         print("Modeling distribution of species '%s'" % installer.name)

    #         # Standardize features

    #         mean = installer.cov_train.mean(axis=0)
    #         std = installer.cov_train.std(axis=0)
    #         train_cover_std = (installer.cov_train - mean) / std

    #         # Fit OneClassSVM
    #         print(" - fit OneClassSVM ... ", end='')
    #         clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.5)
    #         clf.fit(train_cover_std)
    #         print("done.")

    #         print(" - plot coastlines from coverage")



    #         axarr[0][i].contour(X, Y, land_reference, levels=[-9999], colors="k", linestyles="solid")
    #         # plot_polygon(axarr[i], geometry, color='w', alpha=0.5)

    #         axarr[0][i].axes.get_xaxis().set_visible(False)
    #         axarr[0][i].axes.get_yaxis().set_visible(False)

    #         Z = np.ones((data.Ny, data.Nx), dtype=np.float64)

    #         # We'll predict only for the land points.
    #         idx = np.where(land_reference > -9999)
    #         coverages_land = data.coverages[:, idx[0], idx[1]].T

    #         pred = clf.decision_function((coverages_land - mean) / std)[:, 0]

    #         Z *= pred.min()
    #         Z[idx[0], idx[1]] = pred

    #         levels = np.linspace(Z.min(), Z.max(), 25)
    #         Z[land_reference == -9999] = -9999
    #         axarr[0][i].scatter(installer.pts_train['x'], installer.pts_train['y'], s=2 ** 2, c='black', marker='^', label='train')
    #         axarr[0][i].scatter(installer.pts_test['x'], installer.pts_test['y'], s=2 ** 2, c='black', marker='x', label='test')


    #         # plot contours of the prediction
    #         axarr[0][i].contourf(X, Y, Z, levels=levels, cmap=plt.cm.Reds)
            
    #         # axarr[count].colorbar(format='%.2f')


    #         axarr[0][i].legend()
    #         axarr[0][i].set_title(installer.name)
    #         axarr[0][i].axis('equal')


    #         # Compute AUC w.r.t. background points
    #         pred_background = Z[background_points[0], background_points[1]]
    #         pred_test = clf.decision_function((installer.cov_test - mean) / std)[:, 0]

    #         scores = np.r_[pred_test, pred_background]
    #         y = np.r_[np.ones(pred_test.shape), np.zeros(pred_background.shape)]
    #         axarr[1][i].set_aspect(2)

    #         # Plot ROC curve


    #         fpr, tpr, thresholds = metrics.roc_curve(y, scores)
    #         roc_auc = metrics.auc(fpr, tpr)


    #         axarr[1][i].plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    #         axarr[1][i].plot([0, 1], [0, 1], 'k--')
    #         # axarr[1][i].xlim([0.0, 1.0])
    #         # axarr[1][i].ylim([0.0, 1.0])
    #         axarr[1][i].xlabel('False Positive Rate')
    #         axarr[1][i].ylabel('True Positive Rate')
    #         # axarr[2][i].title('Receiver operating characteristic example')
    #         axarr[1][i].legend(loc="lower right")



    #         print("\nArea under the ROC curve : %f" % roc_auc)

    #     except Exception as e:
    #         print(e)



    plt.show()


if __name__ == '__main__':
    county_name = 'harris'
    square_size = 10000
    main(county_name, square_size)

