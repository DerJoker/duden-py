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

	def __init__(self, column):
		self.reader = csv.DictReader(open(fn_alphabet_csv))
		self.columns = self.reader.fieldnames
		self.fieldname_rechtschreibung = 'rechtschreibung'
		self.column = column

	def get_none_empty_list(self):
		lst = []
		if self.column in self.columns:
			for row in self.reader:
				if row[self.column] != '':
					lst.append(row[self.fieldname_rechtschreibung])
		return lst

if __name__ == '__main__':
	alphacsv = AlphabetCSV('aussprache')
	print alphacsv.column
	print alphacsv.get_none_empty_list()
	alphacsv = AlphabetCSV('star')
	print alphacsv.column
	print alphacsv.get_none_empty_list()