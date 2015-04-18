# coding: UTF-8

import os

import config

from duden import Rechtschreibung
from duden import Analyser
from anki import CardExample

def makeCardsExample():
    f_anki = open('anki_examples.txt','w')
    lsLocal = os.listdir(config._path_rechtschreibung)
    for local in lsLocal:
        if str(local).endswith('.html'):
            analyser = Analyser(open(os.path.join(config._path_rechtschreibung, local)).read())
            word = analyser.getWord()
            mp3 = local.replace('.html','.mp3')
            examples = analyser.getExamples()
            for key in examples:
                for example in examples[key]:
#                     print example
                    ce = CardExample(example,word,key,mp3)
                    print ce.printCardExample()
                    f_anki.write(ce.printCardExample().encode('utf-8'))
    f_anki.close()

def makeCardsExampleZD():
    f_anki = open('anki_examples.txt','w')
    lsLocal = os.listdir(config._path_rechtschreibung)
    for local in lsLocal:
        if str(local).endswith('.html'):
            analyser = Analyser(open(os.path.join(config._path_rechtschreibung, local)).read())
            if analyser.is_Wortschatz_des_Zertifikats_Deutsch():
                word = analyser.getWord()
                print word
                mp3 = local.replace('.html','.mp3')
                examples = analyser.getExamples()
                for key in examples:
                    for example in examples[key]:
                        ce = CardExample(example,word,key,mp3)
                        f_anki.write(ce.printCardExample().encode('utf-8'))
    f_anki.close()

if os.path.exists(config._path_rechtschreibung) == False:
    os.mkdir(config._path_rechtschreibung)
    print 'path', config._path_rechtschreibung, 'created'

lsLocal = os.listdir(config._path_rechtschreibung)
lsRS = []

if lsLocal == []:
    # seed
    lsRS.extend([u'abfahren', u'Bild'])
    # ...

# makeCardsExample()
makeCardsExampleZD()

# lsRS = list(set(lsRS))
# print 'lsRS:', len(lsRS)