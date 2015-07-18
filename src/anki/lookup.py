# coding: UTF-8

import csv
import os

from duden import Duden, Rechtschreibung

# file name
fn = 'anki.csv'
fn_bak = 'anki.bak.csv'

FieldNames = ['id_wt','wort','aktualisiert','id_rs','rechtschreibung','zertifikat',
              'id_bd','bedeutung','id_bs','beispiel','star','stufe']

class AnkiRow:
    
    def __init__(self, dt_anki):
        self.dt_anki = dt_anki
    
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
                self.dt_anki['id_rs'] = str(i)
                self.dt_anki['rechtschreibung'] = ls_rs[i]
                
                rechtschreibung = Rechtschreibung(ls_rs[i])
                # zertifikat not implemented yet, default ''
                
                # list tuple (beispiel, bedeutung)
                ls_tbd= rechtschreibung.getTupleExampleAndDefinition()
                if len(ls_tbd) == 0: # keep this record/row even if empty
                    ls_tbd = [('','')]  # initialize to '', dealt with in the following for-loop
                
                for (beispiel, bedeutung) in ls_tbd:
                    self.dt_anki['beispiel'] = beispiel
                    self.dt_anki['bedeutung'] = bedeutung
                    self.dt_anki['beispiel'] = 'beispiel'
                    self.dt_anki['bedeutung'] = 'bedeutung'
                    
                    res.append(self.dt_anki)
        
        # updated, return as it is
        else: print res.append(self.dt_anki)
        
        return res

# read & write
with open(fn_bak) as csv_bak:
    with open(fn, 'w') as csv_file:
        reader = csv.DictReader(csv_bak)
        writer = csv.DictWriter(csv_file, fieldnames=FieldNames)
        writer.writeheader()
        
        for row in reader:
            print row['id_wt']
            rows =  AnkiRow(row).extend()
            print rows
#             rows = [item.decode('utf-8') for row in rows for item in row]
            writer.writerows(rows)