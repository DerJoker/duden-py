#!/usr/bin/python

import json

import Dict

DUDEN = 'Duden.json'
MYDICT = 'MyDict.json'
GODIC = 'Godic.json'

wdList1 = ['verlangen', 'schweben', 'verzahnen', 'abwarten', 'hocken', 'Schlacht', 'Anhaltspunkt', 'Kabine', 'dick', 'getreu', 'tilgen', 'teilen']
wdList2 = ['Schlacht', '', 'Kabine', 'dick', 'getreu', 'tilgen', 'teilen', 'Pleit', 'Nische', 'Akteur', 'mitgenommen', 'Abrechnung', 'Wucht', 'verlaufen', 'anwidern', 'voraussagen', 'einnehmend', 'hineinversetzen']

wdList3 = list(set(wdList1 + wdList2))
print len(wdList3)

# try:
#     d_test = json.load(open(GODIC))
#     d_duden = json.load(open(DUDEN))
# except:
#     d_test = {}
#     d_duden = {}

d_test = {}
d_duden = {}

left_godic = []

print 'search wdList1: ', len(wdList1)

for word in wdList1:
    if word != '':
        dictest = Dict.Duden(word)
        dictest.lookup()
        if dictest.displays != []:
            d_test.update(dictest.createDictEntry())
        else:
            left_godic.append(word)

json.dump(d_test, open(DUDEN, 'w'))

print 'search wdList2: ', len(wdList2)

for word in wdList2:
    if word != '':
        dictest = Dict.Duden(word)
        dictest.lookup()
        if dictest.displays != []:
            d_test.update(dictest.createDictEntry())
        else:
            left_godic.append(word)

json.dump(d_test, open(DUDEN, 'w'))

d_test = json.load(open(DUDEN))
print len(d_test)

print set(wdList3) - set(d_test.keys())

print left_godic
