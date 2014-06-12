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

		for num in range(len(self.features)):

			prop_id = self.features[num]['properties']["HCAD_NUM"]
			
			p = self.match_property(prop_id, self.res)
			if p[0] == True:
				self.write_to_json_res(num, p[1])

		
			elif p[0] == False:
				print "trying other"
				p = self.match_property(prop_id, self.other)

		self.write_json('stuff.json', self.features)



	def match_property(self, prop_id, filename):
		p = None
		filename.seek(0)

		in_list = False

		for prop in filename:
			p = prop.split('\t')
			

			if p[0].replace(' ','') == prop_id:
				print p[0], prop_id
				in_list = True
				break
		
		return in_list, p


	def write_to_json_res(self, num, data):
		self.features[num]['properties']['USE_CODE'] = data[2]
		self.features[num]['properties']['renting'] = data[3]



		print len(data)

	def write_json(self, filename, dictionary):
		print "writing file: ", filename
		with open(filename, 'wb') as fp:
			json.dump(dictionary, fp, indent=4, sort_keys=True)







def main():
	other = '/Users/mattstringer/research/Houston_analysis/data/text_folder/building_other.txt'
	res = '/Users/mattstringer/research/Houston_analysis/data/text_folder/building_res.txt'
	features = '/Users/mattstringer/research/Houston_analysis/houston_short.json'

	c = checkFile(res, other, features)
	c.run_features()




if __name__ == '__main__':
	main()