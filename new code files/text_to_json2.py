import json
import re
input=open('C:/Users/Prateek Raj/Desktop/houston_analysis/data/building_res.txt','r')
output=open('C:/Users/Prateek Raj/Desktop/houston_analysis/data/json_res.json','w')
str="1"
count=0
bad=0
ls=[]
fields=["Ac", "UC","BN","IT","BSC","CS","CSD","DV","CRC","ADP","QLT","QD","DE", "ED","YRM","YRL","AB","AD","NOTE","ISF","AA","HA","GA","EA","BA","PM","PC","NF","RC","SI","LSA"]
while(str):
	str=input.readline()
	parts=str.split('\t')
	if len(parts)==31:
		d={}
		p=parts[0]
		d.update({"Ac":p.strip()})
		p=parts[3]
		d.update({"IT":p.strip()})
		count=count+1
		json.dump(d, output)
		output.write(",\n")
	else:
		print str
		bad=bad+1
		count=count+1
		print bad
	count=count+1



print 'done!!'