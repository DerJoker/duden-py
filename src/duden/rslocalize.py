'''
Created on Aug 7, 2015

@author: feng

Based on alphabet.csv, save all the pages to folder rechtschreibung
'''

import os.path
import csv

import local
save_rechtschreibung = local.save_rechtschreibung

alphabet_csv = 'alphabet.csv'

URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'

if __name__ == '__main__':
    
    cnt_save_ok = 0
    cnt_wort = len(open(alphabet_csv).readlines()) - 1
    
    with open(alphabet_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            wort_rs = row['rechtschreibung']
            print wort_rs
            link = URLRECHTSCHREIBUNG + wort_rs
            html_name = wort_rs + '.html'
            if save_rechtschreibung(link, html_name):
                cnt_save_ok += 1
    
    if cnt_save_ok < cnt_wort:
        print cnt_wort - cnt_save_ok, 'left'
        print 'please rerun this script...'
    else: print 'download rechtschreibung pages complete.'