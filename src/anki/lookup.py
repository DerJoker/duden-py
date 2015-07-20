# coding: UTF-8

import csv
import os
import logging
import copy

from duden import Duden
from anki import AnkiRechtschreibung
from bs4 import BeautifulSoup

logging.basicConfig(filename='anki_lookup.log',level=logging.DEBUG)

# file name
fn = 'anki.csv'
fn_bak = 'anki.bak.csv'

FieldNames = ['id_wt','wort','aktualisiert','rechtschreibung','zertifikat',
              'bedeutung_text','beispiel_text','star','stufe','bedeutung','beispiel']

class AnkiRow:
    
    def __init__(self, dt_anki):
        self.dt_anki = dt_anki
        self.links = {}
    
    def extend(self):
        '''
        extend the row and fill in all the fields
        if not updated (aktualisiert) yet.
        
        self -> [row, ...]
        '''
        res = []
        
        # yet to update
        if self.dt_anki['aktualisiert'] == '' or self.dt_anki['aktualisiert'] == '0':
            ls_rs = Duden(self.dt_anki['wort']).getRechtschreibung()
            
            if len(ls_rs) == 0: # keep this record/row even if empty (no rechtschreibung found), please check again manually
                self.dt_anki['aktualisiert'] = '0'  # failed to update
                res.append(self.dt_anki)
            else: self.dt_anki['aktualisiert'] = '1'    # updated
            
            for i in range(len(ls_rs)):
                self.dt_anki['rechtschreibung'] = ls_rs[i]
                
                rechtschreibung = AnkiRechtschreibung(ls_rs[i])
                # zertifikat not implemented yet, default ''
                if rechtschreibung.is_Wortschatz_des_Zertifikats_Deutsch():
                    self.dt_anki['zertifikat'] = '1'
                else: self.dt_anki['zertifikat'] = '0'
                # list tuple (beispiel, bedeutung)
                ls_tbd = rechtschreibung.getCardExample()
                self.links.update(rechtschreibung.getLinks())
                
                if len(ls_tbd) == 0: # keep this record/row even if empty
                    ls_tbd = [('','')]  # initialize to '', dealt with in the following for-loop
                
                for (beispiel, bedeutung) in ls_tbd:
                    dt_anki = copy.copy(self.dt_anki)
                    dt_anki['beispiel_text'] = BeautifulSoup(beispiel).get_text().encode('utf-8')
                    dt_anki['bedeutung_text'] = BeautifulSoup(bedeutung).get_text().encode('utf-8')
                    dt_anki['beispiel'] = beispiel.encode('utf-8')
                    dt_anki['bedeutung'] = bedeutung.encode('utf-8')
                    
                    res.append(dt_anki)
        
        # updated, return as it is
        else: print res.append(self.dt_anki)
        
        return res

f_anki_links = open('links.txt', 'w')

# read & write
with open(fn_bak) as csv_bak:
    with open(fn, 'w') as csv_file:
        reader = csv.DictReader(csv_bak)
        writer = csv.DictWriter(csv_file, fieldnames=FieldNames)
        writer.writeheader()
        
        for row in reader:
            logging.info(row['id_wt'])
            ar = AnkiRow(row)
            rows =  ar.extend()
            for value in ar.links.values():
                f_anki_links.write(value + '\n')
            writer.writerows(rows)

f_anki_links.close()