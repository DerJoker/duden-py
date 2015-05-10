# coding: UTF-8

import os

import config

import duden

from duden import Rechtschreibung
from duden import Analyser
from anki import CardExample

'''
functions
'''

def findAllWZD():
    f = open('wzd_list.txt','w')
    for local in lsLocal:
        analyser = Analyser(open(os.path.join(config._path_rechtschreibung, local)).read())
        if analyser.is_Wortschatz_des_Zertifikats_Deutsch():
            rs = local.replace('.html','')
            f.write(rs + '\n')
            print rs
    f.close()

def makeCardsExample():
    f_anki = open('anki_examples.txt','w')
    for local in lsLocal:
        if str(local).endswith('.html'):
            analyser = Analyser(open(os.path.join(config._path_rechtschreibung, local)).read())
            word = analyser.getWord()
            print word
            mp3 = local.replace('.html','.mp3')
            examples = analyser.getExamples()
            for key in examples:
                for example in examples[key]:
                    ce = CardExample(example,word,key,mp3)
                    f_anki.write(ce.printCardExample())
    f_anki.close()

def makeCardsExampleZD():
    f_anki = open('anki_examples_zd.txt','w')
    for local in lsLocal:
        rs = local.replace('.html','')
        analyser = Analyser(open(os.path.join(config._path_rechtschreibung, local)).read())
        if analyser.is_Wortschatz_des_Zertifikats_Deutsch():
            word = analyser.getWord()
            print word
            mp3 = local.replace('.html','.mp3')
            if analyser.getLinkMP3 != None:
                duden.download(analyser.getLinkMP3(), os.path.join(config._path_duden_mp3,mp3))
            examples = analyser.getExamples()
            for key in examples:
                for example in examples[key]:
                    ce = CardExample(rs,example,word,key,mp3)
                    ce.buildFrontStr()
                    ce.buildBackStr()
                    f_anki.write(ce.makeCard())
    f_anki.close()

def moreRechtschreibung(lsLocal):
    lsRS = []
    if lsLocal == []:
        # seed
        lsRS.extend([u'abfahren', u'Bild'])
    
    for local in lsLocal:
        analyser = Analyser(open(os.path.join(config._path_rechtschreibung, local)).read())
        lsRS.extend(analyser.getRechtschreibungOnPage())
    
    lsRS = list(set(lsRS))
    
    for irs in lsRS:
        print irs
        rs = Rechtschreibung(irs)

'''
main()
'''

if os.path.exists(config._path_rechtschreibung) == False:
    os.mkdir(config._path_rechtschreibung)
    print 'path', config._path_rechtschreibung, 'created'

lsLocal = [item for item in os.listdir(config._path_rechtschreibung) if str(item).endswith('.html')]

findAllWZD()

# makeCardsExample()
# makeCardsExampleZD()

# moreRechtschreibung(lsLocal)