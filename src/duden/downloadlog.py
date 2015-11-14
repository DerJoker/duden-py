# coding: UTF-8

'''
Created on Nov 11, 2015

@author: feng
'''

import csv
import os.path

class DownloadLogEntryFactory():

	def __init__(self):
		self.dict = {}

	def make_entry(self, link, local, check):
		self.dict.update({link : {'link' : link, 'local' : local, 'check' : check}})

	def get_entries(self):
		return self.dict

class DownloadLog():

	fn_download_log_csv = 'download.log.csv'

	fieldnames = ['link', 'local', 'check']

	def __init__(self):

		self.dict = self._read()

	def _read(self, all=True):

		ret = {}

		if not os.path.exists(DownloadLog.fn_download_log_csv):
			self._write({})

		with file(DownloadLog.fn_download_log_csv) as csvfile:
			reader = csv.DictReader(csvfile)
			if all:
				for row in reader:
					# link as key, row (dict) as value
					ret.update({row['link'] : row})
			else:
				for row in reader:
					if row['check'] == 'false':
						ret.update({row['link'] : row})

		return ret

	def _write(self, dict_to_write):
		with file(DownloadLog.fn_download_log_csv, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=DownloadLog.fieldnames)
			writer.writeheader()
			for item in dict_to_write.values():
				writer.writerow({'link' : item['link'], 'local' : item['local'], 'check' : item['check']})

	def export(self):
		'''
		list unsuccessful download
		'''
		return self._read(all=False)

	def update(self, dict_to_update):
		self.dict.update(dict_to_update)
		self._write(self.dict)

if __name__ == '__main__':

	downloadlog = DownloadLog()
	dict_to_update = downloadlog.export()

	# add entries
	factory = DownloadLogEntryFactory()
	factory.make_entry('http', 'file', 'false')
	factory.make_entry('http2', 'file2', 'true')
	factory.make_entry('http3', 'file3', 'false')
	dict_to_update.update(factory.get_entries())

	# edit
	for item in dict_to_update.values():
		item['check'] = 'true'

	downloadlog.update(dict_to_update)
	assert downloadlog.export() == {}