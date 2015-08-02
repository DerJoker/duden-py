'''
Created on Aug 2, 2015

@author: feng
'''

import csv
import os.path

CODEC = 'utf-8'

from rechtschreibung import Rechtschreibung

if __name__ == '__main__':
    
    # read from alphabet.csv
    fn_alphabet_csv = 'alphabet.csv'
    FieldNamesAlphabet = ['wort', 'rechtschreibung']
    
    if not os.path.exists(fn_alphabet_csv):
        with open(fn_alphabet_csv, 'w') as csv_alphabet:
            writer = csv.writer(csv_alphabet)
            writer.writerow(['wort','rechtschreibung'])
            writer.writerow((u'\u20b0'.encode(CODEC), u'd_Korrekturzeichen_fuer_tilgen'))
    
    # start from where it's left
    with open(fn_alphabet_csv) as csv_alphabet:
        reader = csv.reader(csv_alphabet)
        for row in reader:
            row_last = row
        (wort, wort_rs) = (row_last[0], row_last[1])
    
    with open(fn_alphabet_csv, 'a+') as csv_alphabet:
        writer = csv.writer(csv_alphabet)
        
        rows = Rechtschreibung(wort_rs).get_alphabet_danach()
        while rows != []:
            rows_encode = [(wort.encode(CODEC), wort_rs.encode(CODEC)) for (wort, wort_rs) in rows]
            writer.writerows(rows_encode)
            
            wort_rs = rows[-1][1]
            print wort_rs
            rows = Rechtschreibung(wort_rs).get_alphabet_danach()