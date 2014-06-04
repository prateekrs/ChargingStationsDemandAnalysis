
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
    --square_size integer
```


More features can be added to the properties tag.


TODOs for houston_grid_maker.py:
- [ ] add counts for each type of business
- [ ] remove hardcoding in each for file saving
- [ ] Document how to run the file.
- [ ] 
- [ ] 