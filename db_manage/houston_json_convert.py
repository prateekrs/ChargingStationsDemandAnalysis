import sys,os,json
#features = json.load(open(file_name, 'r'))
filename=open('C:/Users/Prateek Raj/Desktop/houston_analysis/houston.json').read()
features = json.loads(filename)
output=open('C:/Users/Prateek Raj/Desktop/houston_analysis/new_houston_main.json','w')
#	str=input.readline()
#	parts=str.split('\t')
#	if len(parts)==31:
#		d={}
#		p=parts[0]
#		d.update({"Ac":p.strip()})
#		p=parts[3]
#		d.update({"IT":p.strip()})
#		count=count+1
for num in range(len(features)):
	d={}
	d.update({"geometry":features[num]['geometry']})
	d.update({"id": features[num]['id']})
	d.update({"properties":features[num]['properties']})
	json.dump(d,output)
	output.write(',\n')

