# coding: UTF-8

'''
Created on Nov 8, 2015

@author: feng
'''

import csv
import os.path

fn_alphabet_csv = 'alphabet.edit.csv'
assert os.path.exists(fn_alphabet_csv)

class AlphabetCSV():

	reader = csv.DictReader(open(fn_alphabet_csv))
	columns = reader.fieldnames
	fieldname_rechtschreibung = 'rechtschreibung'

	def __init__(self, column):
		self.column = column

	def getNoneEmptyList(self):
		lst = []
		if self.column in AlphabetCSV.columns:
			for row in AlphabetCSV.reader:
				if row[self.column] != '':
					lst.append(row[AlphabetCSV.fieldname_rechtschreibung])
		return lst

if __name__ == '__main__':
	alphacsv = AlphabetCSV('v_top50')
	print alphacsv.getNoneEmptyList()