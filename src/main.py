# coding: UTF-8

import os

import config

from duden import Rechtschreibung

if os.path.exists(config._path_rechtschreibung) == False:
    os.mkdir(config._path_rechtschreibung)

lsLocal = os.listdir(config._path_rechtschreibung)
lsRS = []

if lsLocal == []:
    print 'empty'
    # seed
    lsRS.extend([u'abfahren', u'Bild'])
else:
    print 'not empty'
    print lsLocal