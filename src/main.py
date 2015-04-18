# coding: UTF-8

import os

from duden import Rechtschreibung

_path_rechtschreibung = '../rechtschreibung/'

if os.path.exists(_path_rechtschreibung) == False:
    os.mkdir(_path_rechtschreibung)

lsLocal = os.listdir(_path_rechtschreibung)
lsRS = []

if lsLocal == []:
    print 'empty'
    # seed
    lsRS.extend([u'abfahren', u'Bild'])
else:
    print 'not empty'
    print lsLocal