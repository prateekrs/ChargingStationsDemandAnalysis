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

		for num in range(len(self.features))[:2000]:

			prop_id = self.features[num]['properties']["HCAD_NUM"]

			
			p = self.match_property(prop_id, self.res)
			if p[0] == True:
				self.write_to_json_res(num, p[1])

		
			elif p[0] == False:
				print "trying other"
				p = self.match_property(prop_id, self.other)
				if p[0] == True:
					self.write_to_json_other(num, p[1])
				if p[0] == False:
					print "not found!!"	

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
		self.features[num]['properties']['FILE_ORG'] = 'RES'
		self.features[num]['properties']['USE_CODE'] = data[1]
		self.features[num]['properties']['BUILDING_NUMBER'] = data[2]
		self.features[num]['properties']['IMPRV_TYPE'] = data[3]
		self.features[num]['properties']['BUILDING_STYLE_CODE'] = data[4]
		self.features[num]['properties']['CLASS_STRUCTURE'] = data[5]
		self.features[num]['properties']['CLASS_STRUC_DESCRIPTION'] = data[6]
		self.features[num]['properties']['DEPRECIATION VALUE'] = data[7]
		self.features[num]['properties']['CAMA_REPLACEMENT_COST'] = data[8]
		self.features[num]['properties']['ACCRUED_DEPR_PCT'] = data[9]
		self.features[num]['properties']['QUALITY'] = data[10]
		self.features[num]['properties']['QUALITY_DESCRIPTION'] = data[11]
		self.features[num]['properties']['DATE_ERECTED'] = data[12]
		self.features[num]['properties']['EFFECTIVE_DATE'] = data[13]
		self.features[num]['properties']['YR_REMODEL'] = data[14]
		self.features[num]['properties']['YR_ROLL'] = data[15]
		self.features[num]['properties']['APPRAISED_BY'] = data[16]
		self.features[num]['properties']['APPRAISED_DATE'] = data[17]
		self.features[num]['properties']['NOTE'] = data[18]
		self.features[num]['properties']['IMPR_SQ_FT'] = data[19]
		self.features[num]['properties']['ACTUAL_AREA'] = data[20]
		self.features[num]['properties']['HEAT_AREA'] = data[21]
		self.features[num]['properties']['GROSS_AREA'] = data[22]
		self.features[num]['properties']['EFFECTIVE_AREA'] = data[23]
		self.features[num]['properties']['BASE_AREA'] = data[24]
		self.features[num]['properties']['PERIMETER'] = data[25]
		self.features[num]['properties']['PERCENT_COMPLETE'] = data[26]
		self.features[num]['properties']['NBHD_FACTOR'] = data[27]
		self.features[num]['properties']['RCNLD'] = data[28]
		self.features[num]['properties']['SIZE-INDEX'] = data[29]
		self.features[num]['properties']['LUMP_SUM_ADJ'] = data[30]
		print len(data)

	def write_to_json_other(self, num, data):
		self.features[num]['properties']['FILE_ORG'] = 'OTHER'
		self.features[num]['properties']['USE_CODE'] = data[1]
		self.features[num]['properties']['BUILDING_NUMBER'] = data[2]
		self.features[num]['properties']['IMPRV_TYPE'] = data[3]
		self.features[num]['properties']['BUILDING_STYLE_CODE'] = data[4]
		self.features[num]['properties']['CLASS_STRUCTURE'] = data[5]
		self.features[num]['properties']['CLASS_STRUC_DESCRIPTION'] = data[6]
		self.features[num]['properties']['NOTICED_DEPR_VALUE'] = data[7]
		self.features[num]['properties']['DEPRECIATION_VALUE'] = data[8]
		self.features[num]['properties']['MS_REPLACEMENT_COST'] = data[9]
		self.features[num]['properties']['CAMA_REPLACEMENT_COST'] = data[10]
		self.features[num]['properties']['ACCRUED_DEPR_PCT'] = data[11]
		self.features[num]['properties']['QUALITY'] = data[12]
		self.features[num]['properties']['QUALITY_DESCRIPTION'] = data[13]
		self.features[num]['properties']['DATE_ERECTED'] = data[14]
		self.features[num]['properties']['EFFECTIVE_DATE'] = data[15]
		self.features[num]['properties']['YR_REMODEL'] = data[16]
		self.features[num]['properties']['YR_ROLL'] = data[17]
		self.features[num]['properties']['APPRAISED_BY'] = data[18]
		self.features[num]['properties']['APPRAISED_DATE'] = data[19]
		self.features[num]['properties']['NOTE'] = data[20]
		self.features[num]['properties']['IMPR_SQ_FT'] = data[21]
		self.features[num]['properties']['ACTUAL_AREA'] = data[22]
		self.features[num]['properties']['HEAT_AREA'] = data[23]
		self.features[num]['properties']['GROSS_AREA'] = data[24]
		self.features[num]['properties']['EFFECTIVE_AREA'] = data[25]
		self.features[num]['properties']['BASE_AREA'] = data[26]
		self.features[num]['properties']['PERIMETER'] = data[27]
		self.features[num]['properties']['PERCENT_COMPLETE'] = data[28]
		self.features[num]['properties']['CATEGORY'] = data[29]
		self.features[num]['properties']['CATEGORY_DSCR'] = data[30]
		self.features[num]['properties']['PROPERTY_NAME'] = data[31]
		self.features[num]['properties']['UNITS'] = data[32]
		self.features[num]['properties']['NET_RENT_AREA'] = data[33]
		self.features[num]['properties']['LEASE_RATE'] = data[34]
		self.features[num]['properties']['OCCUPANCY_RATE'] = data[35]
		self.features[num]['properties']['TOTAL_INCOME'] = data[36]
		print len(data)

	def write_json(self, filename, dictionary):
		print "writing file: ", filename
		with open(filename, 'wb') as fp:
			json.dump(dictionary, fp, indent=4, sort_keys=True)

def main():
#	other = '/Users/mattstringer/research/Houston_analysis/data/text_folder/building_other.txt'
#	res = '/Users/mattstringer/research/Houston_analysis/data/text_folder/building_res.txt'
#	features = '/Users/mattstringer/research/Houston_analysis/houston_short.json'

	other = 'C:/Users/Prateek Raj/Desktop/houston_analysis/data/building_other.txt'
	res = 'C:/Users/Prateek Raj/Desktop/houston_analysis/data/building_res.txt'
	features = 'C:/Users/Prateek Raj/Desktop/houston_analysis/houston_short.json'



	c = checkFile(res, other, features)
	c.run_features()




if __name__ == '__main__':
	main()