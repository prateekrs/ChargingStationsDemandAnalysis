Data Processing Scripts 
============
Below is a list of files and the order they should be ran.
1. grid_maker.py - runs pymongo file for Houston converting each feature into a separate raster file. Theses files are stored in /data/raster_files. Features are the agglomeration of points to form a 



```bash
$ python grid_maker.py --county_name "(name of county being analyzed - string)" --square_size "(size of squares float)"
```

List of Raster Files made to 
    - tot_num_amusementpark.asc
    - tot_num_banks.asc
    ─ tot_num_buildings.asc
    ─ tot_num_cardealership.asc
    ─ tot_num_condos.asc
    ─ tot_num_correctional.asc
    ─ tot_num_electriccompany.asc
    ─ tot_num_emergencystation.asc
    ─ tot_num_gascompany.asc
    ─ tot_num_industrial.asc
    ─ tot_num_library.asc
    ─ tot_num_medical.asc
    ─ tot_num_offices.asc
    ─ tot_num_pipeline.asc
    ─ tot_num_postoffice.asc
    ─ tot_num_railroad.asc
    ─ tot_num_recreation.asc
    ─ tot_num_religious.asc
    ─ tot_num_residential.asc
    ─ tot_num_restaurant.asc
    ─ tot_num_shopping.asc
    ─ tot_num_social.asc
    ─ tot_num_telephone.asc
    ─ tot_num_theatres.asc
    ─ tot_num_transport.asc
    ─ tot_num_warehouse.asc




2. make_bunches.py - opens all relevant files  used in the model and puts these files in a numpy arrays in a bunch (an sklearn data type.)
    relevant files added include:
    - all raster files 
    - time series data for charging stations that includes usage for each month since start of operation.

    Metadata extracted
    - x_left_lower_corner
    - Nx=header['ncols'],
    - y_left_lower_corner
    - Ny
    - grid_size


3. model.py - makes a csv file that is used in the regression. It converts the raster data into independent variables used in the model.

my_libraries
============

These additional libraries that are used in the analysis.

- filemanage.py - is an ancillary file that manages loading and saving data files in various formats
- squaremaker.py - defines the spatial x and y limits for the study area. There are also functions for making a map in matplotlib.






Data Prep
==========


data_analysis
============






The geoJSON files for all the building is this format

```javascript
{
    "geometry": {
        "coordinates": [
            3055694.437321233, 
            13812156.730583059
        ], 
        "type": "Point"
    }, 
    "id": null, 
    "properties": {
        "BLK_NUM": null, 
        "CONDO_FLAG": "0", 
        "CurrOwner": "BELLO JUAN A", 
        "HCAD_NUM": "1004280000028", 
        "LOT_NUM": null, 
        "LocAddr": "8610 LEAMONT DR", 
        "LocName": "LEAMONT", 
        "LocNum": 8610, 
        "city": "HOUSTON", 
        "parcel_typ": 0, 
        "zip": "77099"
    }, 
    "type": "Feature"
}, 
```



