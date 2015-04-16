# coding: UTF-8

import Queue
from duden import Rechtschreibung

from anki import CardImg
from anki import CardIdiom
from anki import CardExample

done = 'done.txt'
pool = 'pool.txt'
rs = 'rechtschreibung.txt'

def readList(txt):
    try:
        return eval(open(txt,'r').read())
    except:
        return []

def writeList(l,txt):
    f = open(txt,'w')
    f.write(str(l))
    f.close()

t_rechtschreibung = 'sicher_gefahrlos_tadellos_garantiert'
# t_rechtschreibung = 'Fall_stuerzen_hinfallen_Sache'
# t_rechtschreibung = 'schlimm'
# t_rechtschreibung = 'Moment_Zeitpunkt_Zeitspanne'
# t_rechtschreibung = 'Richtung'
# t_rechtschreibung = 'blosz_Adjektiv'

ldone = readList(done)
print ldone
tmp = readList(rs)
print tmp

if len(tmp) == 0:
    tmp.append(t_rechtschreibung)

lrs = []

for item in tmp:
    if item not in ldone:
        ldone.append(item)
        
        irs = Rechtschreibung(item)
        irs.downloadMP3()
        for card in irs.makeCardExample():
            print card
        
        lrs.extend(irs.getRechtschreibungOnPage())

lrs.extend(tmp)

lrs = list(set(lrs))
print lrs
print len(lrs)
writeList(lrs, rs)
writeList(ldone, done)