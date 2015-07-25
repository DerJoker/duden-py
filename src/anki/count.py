'''
Created on Jul 25, 2015

@author: feng
'''

import csv
import string

import config

# file name
fn = config.fn

FieldNames = config.FieldNames

res = {}
strips = string.whitespace + string.digits + "\"'[]() +-.,:;!%"

def countWord(line):
    for word in line.split():
        word = word.strip(strips)
        if word != '':
            res[word] = 1 + res.get(word, 0)

with open(fn) as csv_file:
    reader = csv.DictReader(csv_file)
    
    last_bedeutung = ''
    
    for row in reader:
        print row['id_wt'], ' ', row['wort']
        bedeutung_text = row['bedeutung_text']
        beispiel_text = row['beispiel_text']
        
        if last_bedeutung != bedeutung_text:
            last_bedeutung = bedeutung_text
            countWord(bedeutung_text)
        
        countWord(beispiel_text)

with open('count.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['word','count'])
    
    keys = sorted(res.keys())
    for key in keys:
        writer.writerow([key,res[key]])