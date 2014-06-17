Data Processing Scripts 
============
Below is a list of files and the order they should be ran.
1. houston_grid_maker.py - runs geoJSON file for Houston converting each feature into a separate raster file. Theses files are stored in /data/raster_files. The file houston_grid_maker2.py can be alternatively used if there are problems running from the command line.
2. make_bunches.py - opens all relevant files used in the model and puts these files in a numpy arrays in a bunch (an sklearn data type.)
3. [grid]svm.py - runs the SVM model and outputs a graph.

- filemanage.py - is an ancillary file that manages loading and saving data files in various formats
- squaremaker.py - defines the spatial x and y limits for the study area. There are also functions for making a map in matplotlib.








Date Prep
==========





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



```bash
$ python "${Houston_analysis}/code/houston_grid_maker.py" \
    --county_name "county in study" \
    --square_size integer \
    --json_file "absolute path to file"
```


More features can be added to the properties tag.


TODOs for houston_grid_maker.py:
- [ ] add counts for each type of business
- [ ] remove hardcoding in each for file saving
- [ ] Document how to run the file.
- [ ] 
- [ ] 