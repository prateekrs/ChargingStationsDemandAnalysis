import multiprocessing
import pymongo
import os

client = pymongo.MongoClient("localhost")
db=client["full_houston"]

print db.collection_names()
db.houston.ensure_index('properties.HCAD_NUM')
db.impcodes.ensure_index('Ac')
count=0
bad=0



for rec in db.houston.find(timeout=False):
    count=count+1
    print count
    ac=rec['properties']['HCAD_NUM']
    try:
        acint=int(ac)
        mydict=db.impcodes.find_one({"Ac":acint})
        if not mydict==None:
            #db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.DE': mydict['DE']}})
            db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.BT': mydict['BT'],'properties.DE': mydict['DE']}})
        else:
            #db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.DE': "NA"}})
            #db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.BT': "NA"},'$set': {'properties.DE': "NA"}})
            db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.BT': "NA",'properties.DE': "NA"}})
    except:
        bad=bad+1
        #db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.DE': "NA"}})
        db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.BT': "NA",'properties.DE': "NA"}})
        
print bad
"""
count=0
for rec in db.houston.find():
    count=count+1
    print count
    #print rec
    print rec['properties']['BT']
    print rec['properties']['DE']         
""" 
