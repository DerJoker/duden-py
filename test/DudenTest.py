# coding: UTF-8

import Queue
from duden import Rechtschreibung

from anki import CardImg
from anki import CardIdiom
from anki import CardExample

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
# t_rechtschreibung = 'Moment_Zeitpunkt_Zeitspanne'
t_rechtschreibung = 'Richtung'
t_rechtschreibung = 'blosz_Adjektiv'

rs = Rechtschreibung(t_rechtschreibung)

print rs.wort

# l = rs.getRechtschreibungOnPage()
# 
# for item in l:
#     print item
#     irs = Rechtschreibung(item)
#     
#     irs.downloadMP3()
#     
#     for card in irs.makeCardExample():
#         print card
#         print '\n'