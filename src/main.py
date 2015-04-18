# coding: UTF-8

import os

import config

from duden import Rechtschreibung
from duden import Analyser

if os.path.exists(config._path_rechtschreibung) == False:
    os.mkdir(config._path_rechtschreibung)
    print 'path', config._path_rechtschreibung, 'created'

lsLocal = os.listdir(config._path_rechtschreibung)
lsRS = []

if lsLocal == []:
    # seed
    lsRS.extend([u'abfahren', u'Bild'])
    # ...
else:
    for f in lsLocal:
        if str(f).endswith('.html'):
            print f
            analyser = Analyser(open(os.path.join(config._path_rechtschreibung, f)).read())
            lsRS.extend(analyser.getRechtschreibungOnPage())

lsRS = list(set(lsRS))
print 'lsRS:'
print lsRS
print len(lsRS)