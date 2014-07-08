import pymongo
import os

client = pymongo.MongoClient("localhost")
db=client["houston_analysis"]

print db.collection_names()
db.impcodes.ensure_index('Ac')

for rec in db.houston.find():
    ac=rec["properties"]['HCAD_NUM']
    print 'account number=',ac
    mydict=db.impcodes.find_one({"Ac":ac})
    count=db.impcodes.find({"Ac":ac}).count()
    if not mydict==None:
        print 'Account matched=',mydict['Ac']
        print 'Land use code=',mydict['IT']
        print '\n'
    else:
        print 'No match\n'

