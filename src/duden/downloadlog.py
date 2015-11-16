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

	def make_entry(self, link, local, check='false'):
		self.dict.update({link : {'link' : link, 'local' : local, 'check' : check}})


class DownloadLog():

	fn_download_log_csv = 'download.log.csv'

	fieldnames = ['link', 'local', 'check']

	def __init__(self):

		if not os.path.exists(DownloadLog.fn_download_log_csv):
			self._write({}, 'w')

	def _read(self, all=True):

		ret = {}

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

	def _write(self, dict_to_write, mode='a'):
		with file(DownloadLog.fn_download_log_csv, mode) as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=DownloadLog.fieldnames)
			if mode == 'w': writer.writeheader()
			for item in dict_to_write.values():
				writer.writerow({'link' : item['link'], 'local' : item['local'],
								'check' : item['check']})

	def append(self, downloadlog_entry_factory):
		'''
		append new entries to the end
		'''
		self._write(downloadlog_entry_factory.dict)

	def export(self):
		'''
		list unsuccessful download
		'''
		return self._read(all=False)

	def update(self, callback_func):
		'''
		update log.csv
		if callback function returns True, change check to "true"
		'''
		dict = self._read()
		for item in dict.values():
			if item['check'] != 'true' and \
			callback_func(item['link'], item['local']) == True:
				item['check'] = 'true'
				print 'update:', item['link']

		self._write(dict, 'w')


if __name__ == '__main__':

	downloadlog = DownloadLog()

	# add entries
	factory = DownloadLogEntryFactory()
	factory.make_entry('http', 'file', 'false')
	factory.make_entry('http2', 'file2', 'true')
	factory.make_entry('http3', 'file3')

	downloadlog.append(factory)

	# callback
	def always_true(link, local):
		return True

	downloadlog.update(always_true)

	assert downloadlog.export() == {}