import json

import argparse
import textwrap








class checkFile:

	def __init__(self,res,other, features):
		self.res = self.open_file(res)
		self.other = self.open_file(other)
		self.features = self.open_json(features)


	def open_file(self, file_name):
		f = open(file_name,'r')
		return f

	def open_json(self, file_name):
		features = json.load(open(file_name, 'r'))
		return features


	def run_features(self):
		print "running"
		for num in range(len(self.features)):

			prop_id = self.features[num]['properties']["HCAD_NUM"]

			p = self.match_property(prop_id)

	def match_property(self, prop_id):
		p = None
		print 'called'
		self.res.seek(0)
		for prop in self.res:
			p = prop.split('\t')

			print prop_id, p[0].replace(' ','')
			if p[0].replace(' ','') == prop_id:
				print p[0], prop_id
				break
		return p




def main():
	other = '/Users/mattstringer/research/Houston_analysis/data/text_folder/building_other.txt'
	res = '/Users/mattstringer/research/Houston_analysis/data/text_folder/building_res.txt'
	features = '/Users/mattstringer/research/Houston_analysis/houston_short.json'

	c = checkFile(res, other, features)
	c.run_features()




if __name__ == '__main__':
	main()