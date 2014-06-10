import json

features = json.load(open('C:\Users\Prateek Raj\Desktop\houston_analysis\houston_short.json', 'r'))

res='C:/Users/Prateek Raj/Desktop/houston_analysis/data/building_res.txt'
fres=open(res,'r')


other='C:/Users/Prateek Raj/Desktop/houston_analysis/data/building_other.txt'

fother=open(other,'r')


def match_property(prop_id):
	p = None
	print 'called'
	fres.seek(0)

	for prop in fres:
		p = prop.split('\t')
		# print prop_id, p[0].replace(' ','')
		if p[0].replace(' ','') == prop_id:

			print p[0], prop_id
			break

	
			
	return p


for num in range(len(features)):
	prop_id = features[num]['properties']["HCAD_NUM"]

	p = match_property(prop_id)


fres.close()
