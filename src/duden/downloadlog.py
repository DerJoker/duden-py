# coding: UTF-8

'''
Created on Nov 11, 2015

@author: feng
'''

import csv
import os.path
import shutil

class DownloadLog():

	fn_download_log_csv = 'download.log.csv'
	fn_download_log_bk_csv = 'download.log.bk.csv'
	fn_download_log_tmp_csv = 'download.log.tmp.csv'

	fieldnames = ['link', 'local', 'check']

	if not os.path.exists(fn_download_log_csv):
		with open(fn_download_log_csv, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()

	with open(fn_download_log_tmp_csv, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

	@staticmethod # private?
	def write(dict):
		with open(DownloadLog.fn_download_log_csv, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=DownloadLog.fieldnames)
			writer.writeheader()
			for item in dict.values():
				writer.writerow({'link' : item['link'], 'local' : item['local'], 'check' : item['check']})

	@staticmethod
	def addEntry(link, local, check):
		'''
		add an entry to tmp file
		'''
		with open(DownloadLog.fn_download_log_tmp_csv, 'a') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=DownloadLog.fieldnames)
			writer.writerow({'link' : link, 'local' : local, 'check' : check})

	@staticmethod
	def merge():
		'''
		merge tmp file to log file
		'''
		dict = {}

		# firstly, tmp file
		with open(DownloadLog.fn_download_log_tmp_csv, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				dict.update({row['link'] : row})

		# log file (or log bk file) has higher priority
		shutil.copyfile(DownloadLog.fn_download_log_csv, DownloadLog.fn_download_log_bk_csv)
		with open(DownloadLog.fn_download_log_bk_csv, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				dict.update({row['link'] : row})

		DownloadLog.write(dict)

	@staticmethod
	def download():
		'''
		downlad & update the log
		'''
		pass

	@staticmethod
	def report():
		'''
		list unsuccessful download
		'''
		with open(DownloadLog.fn_download_log_csv, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['check'] == 'false':
					print row

if __name__ == '__main__':
	DownloadLog.addEntry('http', 'file', 'false')
	DownloadLog.addEntry('http2', 'file2', 'true')
	DownloadLog.addEntry('http3', 'file3', 'false')
	DownloadLog.merge()
	DownloadLog.report()