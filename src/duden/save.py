'''
Created on Aug 7, 2015

@author: feng

Based on alphabet.csv, save all the pages to folder rechtschreibung
'''

import os.path
import csv

import sys
sys.path.append('..')
from tool import download
download_rechtschreibung = download.download

alphabet_csv = 'alphabet.csv'
fdn_rechtschreibung = 'rechtschreibung'

URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'

if __name__ == '__main__':
    
    if not os.path.exists(fdn_rechtschreibung):
        os.makedirs(fdn_rechtschreibung)
    
    with open(alphabet_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            wort_rs = row['rechtschreibung']
            print wort_rs
            link = URLRECHTSCHREIBUNG + wort_rs
            local = os.path.join(fdn_rechtschreibung, wort_rs + '.html')
            if not os.path.exists(local):
                download_rechtschreibung(link, local)