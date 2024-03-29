import os, sys
#import geojson
from pyproj import Proj, transform
#from shapely.geometry import shape, Point, MultiPoint, LineString
import numpy as np

#from descartes.patch import PolygonPatch

import matplotlib.pyplot as plt
from filemanage import get_directories


datadir, resultsdir = get_directories()

def get_features():
    jsonfile = os.path.join(datadir, 'maps/ca_zip_codes.json')
    map_json = geojson.load(open(jsonfile))
    return map_json['features']

zip_counties = {'San Francisco' :['94102', '94103', '94104', '94105', '94107', '94108', '94109', '94110', '94111', '94112', '94114', '94115', '94116', '94117', '94118', '94121', '94122', '94123', '94124', '94127', '94129', '94130', '94131', '94132', '94134', '94158', '94133'],
                'Los Angeles': [ '90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90009', '90010', '90011', '90012', '90013', '90014', '90015', '90016', '90017', '90018', '90019', '90020', '90021', '90022', '90023', '90024', '90025', '90026', '90027', '90028', '90029', '90030', '90031', '90032', '90033', '90034', '90035', '90036', '90037', '90038', '90039', '90040', '90041', '90042', '90043', '90044', '90045', '90046', '90047', '90048', '90049', '90050', '90051', '90052', '90053', '90054', '90055', '90056', '90057', '90058', '90059', '90060', '90061', '90062', '90063', '90064', '90065', '90066', '90067', '90068', '90069', '90070', '90071', '90072', '90073', '90074', '90075', '90076', '90077', '90078', '90079', '90080', '90081', '90082', '90083', '90084', '90086', '90087', '90088', '90089', '90091', '90093', '90094', '90095', '90096', '90097', '90099', '90101', '90102', '90103', '90174', '90185', '90201', '90202', '90209', '90210', '90211', '90212', '90213', '90220', '90221', '90222', '90223', '90224', '90230', '90231', '90232', '90233', '90239', '90240', '90241', '90242', '90245', '90247', '90248', '90249', '90250', '90251', '90254', '90255', '90260', '90261', '90262', '90263', '90264', '90265', '90266', '90267', '90270', '90272', '90274', '90275', '90277', '90278', '90280', '90290', '90291', '90292', '90293', '90294', '90295', '90296', '90301', '90302', '90303', '90304', '90305', '90306', '90307', '90308', '90309', '90310', '90311', '90312', '90313', '90397', '90398', '90401', '90402', '90403', '90404', '90405', '90406', '90407', '90408', '90409', '90410', '90411', '90501', '90502', '90503', '90504', '90505', '90506', '90507', '90508', '90509', '90510', '90601', '90602', '90603', '90604', '90605', '90606', '90607', '90608', '90609', '90610', '90612', '90637', '90638', '90639', '90640', '90650', '90651', '90652', '90659', '90660', '90661', '90662', '90665', '90670', '90671', '90701', '90702', '90703', '90706', '90707', '90710', '90711', '90712', '90713', '90714', '90715', '90716', '90717', '90723', '90731', '90732', '90733', '90734', '90744', '90745', '90746', '90747', '90748', '90749', '90801', '90802', '90803', '90804', '90805', '90806', '90807', '90808', '90809', '90810', '90813', '90814', '90815', '90822', '90831', '90832', '90833', '90834', '90835', '90840', '90842', '90844', '90845', '90846', '90847', '90848', '90853', '90888', '91001', '91003', '91006', '91007', '91009', '91010', '91011', '91012', '91016', '91017', '91020', '91021', '91023', '91024', '91025', '91030', '91031', '91040', '91041', '91042', '91043', '91046', '91050', '91051', '91066', '91077', '91101', '91102', '91103', '91104', '91105', '91106', '91107', '91108', '91109', '91110', '91114', '91115', '91116', '91117', '91118', '91121', '91123', '91124', '91125', '91126', '91129', '91131', '91175', '91182', '91184', '91185', '91186', '91187', '91188', '91189', '91191', '91201', '91202', '91203', '91204', '91205', '91206', '91207', '91208', '91209', '91210', '91214', '91221', '91222', '91224', '91225', '91226', '91301', '91302', '91303', '91304', '91305', '91306', '91307', '91308', '91309', '91310', '91311', '91312', '91313', '91316', '91321', '91322', '91324', '91325', '91326', '91327', '91328', '91329', '91330', '91331', '91333', '91334', '91335', '91337', '91340', '91341', '91342', '91343', '91344', '91345', '91346', '91350', '91351', '91352', '91353', '91354', '91355', '91356', '91357', '91363', '91364', '91365', '91367', '91371', '91372', '91376', '91380', '91381', '91382', '91383', '91384', '91385', '91386', '91388', '91392', '91393', '91394', '91395', '91396', '91399', '91401', '91402', '91403', '91404', '91405', '91406', '91407', '91408', '91409', '91410', '91411', '91412', '91413', '91416', '91423', '91426', '91436', '91470', '91482', '91495', '91496', '91497', '91499', '91501', '91502', '91503', '91504', '91505', '91506', '91507', '91508', '91510', '91521', '91522', '91523', '91526', '91601', '91602', '91603', '91604', '91605', '91606', '91607', '91608', '91609', '91610', '91611', '91612', '91614', '91615', '91616', '91617', '91618', '91702', '91706', '91711', '91714', '91715', '91716', '91722', '91723', '91724', '91731', '91732', '91733', '91734', '91735', '91740', '91741', '91744', '91745', '91746', '91747', '91748', '91749', '91750', '91754', '91755', '91756', '91759', '91765', '91766', '91767', '91768', '91769', '91770', '91771', '91772', '91773', '91775', '91776', '91778', '91780', '91788', '91789', '91790', '91791', '91792', '91793', '91795', '91797', '91799', '91801', '91802', '91803', '91804', '91841', '91896', '91899', '93510', '93532', '93534', '93535', '93536', '93539', '93543', '93544', '93550', '93551', '93552', '93553', '93563', '93584', '93586', '93590', '93591', '93599'],
                'Fresno': ['93210', '93234', '93242', '93602', '93605', '93606', '93607', '93608', '93609', '93611', '93612', '93613', '93616', '93621', '93622', '93624', '93625', '93626', '93627', '93628', '93630', '93631', '93634', '93640', '93641', '93642', '93646', '93648', '93649', '93650', '93651', '93652', '93654', '93656', '93657', '93660', '93662', '93664', '93667', '93668', '93675', '93701', '93702', '93703', '93704', '93705', '93706', '93707', '93708', '93709', '93710', '93711', '93712', '93714', '93715', '93716', '93717', '93718', '93720', '93721', '93722', '93724', '93725', '93726', '93727', '93728', '93729', '93740', '93741', '93744', '93745', '93747', '93750', '93755', '93759', '93760', '93761', '93762', '93764', '93765', '93771', '93772', '93773', '93774', '93775', '93776', '93777', '93778', '93779', '93780', '93782', '93784', '93786', '93790', '93791', '93792', '93793', '93794', '93844', '93888'],
                'San Diego': ['91901', '91902', '91903', '91905', '91906', '91908', '91909', '91910', '91911', '91912', '91913', '91914', '91915', '91916', '91917', '91921', '91931', '91932', '91933', '91934', '91935', '91941', '91942', '91943', '91944', '91945', '91946', '91947', '91948', '91950', '91951', '91962', '91963', '91976', '91977', '91978', '91979', '91980', '91987', '91990', '92003', '92004', '92007', '92008', '92009', '92013', '92014', '92018', '92019', '92020', '92021', '92022', '92023', '92024', '92025', '92026', '92027', '92028', '92029', '92030', '92033', '92036', '92037', '92038', '92039', '92040', '92046', '92049', '92051', '92052', '92054', '92055', '92056', '92057', '92058', '92059', '92060', '92061', '92064', '92065', '92066', '92067', '92068', '92069', '92070', '92071', '92072', '92074', '92075', '92078', '92079', '92082', '92083', '92084', '92085', '92086', '92088', '92090', '92091', '92092', '92093', '92096', '92101', '92102', '92103', '92104', '92105', '92106', '92107', '92108', '92109', '92110', '92111', '92112', '92113', '92114', '92115', '92116', '92117', '92118', '92119', '92120', '92121', '92122', '92123', '92124', '92126', '92127', '92128', '92129', '92130', '92131', '92132', '92133', '92134', '92135', '92136', '92137', '92138', '92139', '92140', '92142', '92143', '92145', '92147', '92149', '92150', '92152', '92153', '92154', '92155', '92158', '92159', '92160', '92161', '92162', '92163', '92164', '92165', '92166', '92167', '92168', '92169', '92170', '92171', '92172', '92173', '92174', '92175', '92176', '92177', '92178', '92179', '92182', '92184', '92186', '92187', '92190', '92191', '92192', '92193', '92194', '92195', '92196', '92197', '92198', '92199']}

def set_datum():
    cap = Proj('+datum=NAD83 +lat_0=32.10 +lat_1=33.53 '
        '+lat_2=32.47 +lon_0=-116.15 +no_defs +proj=lcc +units=us-ft '
        '+x_0=2000000 +y_0=500000', preserve_units=True)

    wgs84 = Proj(init='epsg:4326')
    return cap, wgs84




def plot_polygon(ax, poly, color='red', alpha=0.5):
    a = np.asarray(poly.exterior)
    # without Descartes, we could make a Patch of exterior
    ax.add_patch(PolygonPatch(poly, facecolor=color, edgecolor='w'))
    ax.plot(a[:, 0], a[:, 1], color='black')

def plot_multipolygon(ax, geom, color='red'):
    """ Can safely call with either Polygon or Multipolygon geometry
    change from original
    """
    if geom.type == 'Polygon':
        plot_polygon(ax, geom, color)
    elif geom.type == 'MultiPolygon':
        for poly in geom.geoms:
            plot_polygon(ax, poly, color)

def spatial_geom(coor):
    xs = []
    ys = []
    cap, wgs84 = set_datum()

    for x in coor:

        if abs(x[0]) < 180.0 and abs(x[1]) < 180.0:
            lat = x[1]
            lon = x[0]


            x, y = transform(wgs84, cap, x[0], x[1])
            xs.append(x)
            ys.append(y)


    cop = {"type": "Polygon", "coordinates": [zip(xs, ys)]}
    return shape(cop)


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


def make_grid(grid_size, features):
    tot_minx=float("inf")
    tot_miny=float("inf")
    tot_maxx=0.0
    tot_maxy=0.0
    

    for feature in features:


        x, y = feature['geometry']["coordinates"]

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

    print "made squares"

    return xgrid, ygrid



def make_study_area_map(county_name, grid_size):
    """Construct the map grid from the county zipcode shapefile

    Parameters
    ----------
    batch : Batch object
        The object returned by :func:`fetch_species_distributions`

    Returns
    -------
    (xgrid, ygrid) : 1-D arrays
        The grid corresponding to the values in batch.coverages
    """
    # fig = plt.figure()
    # fig.add_subplot(111, aspect='equal')
    # ax = fig.gca()

    # area = 0.0
    tot_minx=float("inf")
    tot_miny=float("inf")
    tot_maxx=0.0
    tot_maxy=0.0

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    

    for num in range(len(features)):
        geometry = None
        if features[num]['properties']['ZCTA5CE10'] in zip_counties[county_name]:

            if features[num]['geometry']['type'] == 'Polygon':
                coor = features[num]['geometry']['coordinates'][0]
                geometry = spatial_geom(coor)
                (minx, miny, maxx, maxy) = geometry.bounds
                # plot_polygon(ax, geometry, color='#787878')

            if features[num]['geometry']['type'] == 'MultiPolygon':
                coors = features[num]['geometry']['coordinates']

                for all_coor in coors:
                    for coor in all_coor:
                        geometry = spatial_geom(coor)

            (minx, miny, maxx, maxy) = geometry.bounds
            # plot_polygon(ax, geometry, color='#787878')

            # # make this more pythonic
            if minx < tot_minx:
                tot_minx = minx

            if miny < tot_miny:
                tot_miny = miny

            if maxx > tot_maxx:
                tot_maxx = maxx

            if maxy > tot_maxy:
                tot_maxy = maxy


    # x coordinates of the grid cells
    xgrid = np.arange(tot_minx, tot_maxx, grid_size)
    # y coordinates of the grid cells
    ygrid = np.arange(tot_miny, tot_maxy, grid_size)


    return (xgrid, ygrid, geometry)


def make_county_map(county_name, geobounds=False, color='#787878'):
    jsonfile = os.path.join(datadir, 'maps/ca_counties.json')
    map_json = geojson.load(open(jsonfile))
    features = map_json['features']

    tot_minx=float("inf")
    tot_miny=float("inf")
    tot_maxx=0.0
    tot_maxy=0.0

    # fig = plt.figure()
    # ax = fig.add_subplot(111)

    # may need to add a list here.

    geometry = None

    for num in range(len(features)):

        if features[num]['properties']['NAMELSAD'] == county_name + ' County':


            if features[num]['geometry']['type'] == 'Polygon':
                coor = features[num]['geometry']['coordinates'][0]
                geometry = spatial_geom(coor)
                # (minx, miny, maxx, maxy) = geometry.bounds


            if features[num]['geometry']['type'] == 'MultiPolygon':
                coors = features[num]['geometry']['coordinates']

                for all_coor in coors:
                    for coor in all_coor:
                        geometry = spatial_geom(coor)

            (minx, miny, maxx, maxy) = geometry.bounds
            # plot_polygon(ax, geometry, color)

            if minx < tot_minx:
                tot_minx = minx

            if miny < tot_miny:
                tot_miny = miny

            if maxx > tot_maxx:
                tot_maxx = maxx

            if maxy > tot_maxy:
                tot_maxy = maxy

    square_coors = [(tot_minx, tot_miny), (tot_minx, tot_maxy), (tot_maxx, tot_maxy), (tot_maxx, tot_miny)]
    sqared_geom = {"type": "Polygon", "coordinates": [square_coors]}
    geo_limit = shape(sqared_geom)

    return geometry, geo_limit 

if __name__ == '__main__':

    print make_county_map(county_name='San Diego', geobounds=True)