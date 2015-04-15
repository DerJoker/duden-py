# coding: UTF-8

import Queue
from Duden import Rechtschreibung

from dAnki import CardImg
from dAnki import CardIdiom
from dAnki import CardExample

done = 'done.txt'
pool = 'pool.txt'

def readList(txt):
    return eval(open(txt))

def writeList(l,txt):
    f = open(txt)
    f.write(l)
    f.close()

t_rechtschreibung = 'sicher_gefahrlos_tadellos_garantiert'
# t_rechtschreibung = 'Fall_stuerzen_hinfallen_Sache'
# t_rechtschreibung = 'schlimm'
t_rechtschreibung = 'Moment_Zeitpunkt_Zeitspanne'
t_rechtschreibung = 'Richtung'

rs = Rechtschreibung(t_rechtschreibung)

l = rs.getRechtschreibungOnPage()

for item in l:
    print item
    irs = Rechtschreibung(item)
    
    irs.downloadMP3()
    
    print irs.printAnkiBeispiel()