'''
Created on Aug 6, 2015

@author: feng
'''

import csv

from anki import AnkiRechtschreibung

fn_alphabet_edit_csv = 'alphabet.edit.csv'
fn_anki_result_csv = 'anki.result.csv'

with open(fn_anki_result_csv, 'w') as csv_anki_result:
    pass

f_anki_links = open('links.txt', 'w')
csv_wortschatz_zertifikat = open('wortschatz.zertifikat.txt', 'w')
writer_wz = csv.writer(csv_wortschatz_zertifikat)

if __name__ == '__main__':
    with open(fn_alphabet_edit_csv) as csv_alphabet_edit:
        reader = csv.DictReader(csv_alphabet_edit)
        for row in reader:
            print row['rechtschreibung']
            ars = AnkiRechtschreibung(row['rechtschreibung'])
            if ars.is_Wortschatz_des_Zertifikats_Deutsch():
                writer_wz.writerow([row['wort'], row['rechtschreibung']])
                with open(fn_anki_result_csv, 'a') as csv_anki_result:
                    writer = csv.writer(csv_anki_result)
                    writer.writerows([(beispiel.encode('utf-8'), bedeutung.encode('utf-8'))
                                      for (beispiel, bedeutung) in ars.getCardExample()])
                for value in ars.getLinks().values():
                    f_anki_links.write(value + '\n')