# coding: UTF-8

'''
Created on Nov 28, 2015

@author: feng
'''

import tarfile
import os.path

path_rechtschreibung = os.path.join(os.pardir, os.pardir,
						'data', 'rechtschreibung.tar.gz')
assert os.path.exists(path_rechtschreibung)

with tarfile.open(path_rechtschreibung, 'r:gz') as tar:
	file = tar.extractfile('rechtschreibung/Nationalstaat.html')
	file.read()
	file.close()