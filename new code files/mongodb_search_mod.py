import multiprocessing
import pymongo
import os

client = pymongo.MongoClient("localhost")
db=client["houston_analysis_final"]

print db.collection_names()
db.impcodes.ensure_index('Ac')
count=0

def main():
    num_of_workers = multiprocessing.cpu_count()
    print num_of_workers
    search()
    
def search():
    for rec in db.houston.find(timeout=False):
        count=count+1
        ac=rec['properties']['HCAD_NUM']
        acint=int(ac)
        mydict=db.impcodes.find_one({"Ac":acint})
        if not mydict==None:
            db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.BT': mydict['BT']},'$set': {'properties.DE': mydict['DE']}})
        else:
            db.houston.update({'properties.HCAD_NUM':ac}, {'$set': {'properties.BT': "NA"},'$set': {'properties.DE': "NA"}})


if __name__=='__main__':
    main()
