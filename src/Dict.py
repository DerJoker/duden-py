#!/usr/bin/python

import json
import urllib2
import codecs
from bs4 import BeautifulSoup

# define CONSTANT

CODEC = 'utf-8'

DUDEN = 'Duden.json'
MYDICT = 'MyDict.json'
GODIC = 'Godic.json'

TIMEOUT = 60

class Dict:
    
    def __init__(self, word):
        self.word = word
        self.displays = []
        self.urls = []
        self.definitions = []
    
    def read(self, url):
        try:
            return urllib2.urlopen(url, timeout=TIMEOUT).read()
        except:
            return ''
            print 'Failed to load', url
    
    def getDisplays(self):
        self.displays.append(self.word)
    
    def lookup(self):
        self.getDisplays()
        print self.displays
        self.getURLs()
        print self.urls
        for url in self.urls:
            self.getDefinition(url)
    
    def createDictEntry(self):
        return {self.word: [self.displays, self.urls, self.definitions]}

class Godic(Dict):
    
    URLGODIC = 'http://www.godic.net/dicts/de/'
    
    def getURLs(self):
        self.urls = [Godic.URLGODIC + display for display in self.displays]
    
    def getDefinition(self, url):
        soup = BeautifulSoup(self.read(url))
        try:
            s = str(soup.find('h1', class_='explain-Word'))
            res = soup.find('div', id='tabs--11')  # type <class 'bs4.element.Tag'>
            res.a.decompose()
            s += str(res)
            definition = s.replace('\n', '')
        except:
            definition = ''
            print 'No definition found!'
        self.definitions.append(definition)

class Duden(Dict):
    
    URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'
    URLDUDENONLINE = 'http://www.duden.de/suchen/dudenonline/'
    
    def getDisplays(self):
        try:
            soup = BeautifulSoup(self.read(Duden.URLDUDENONLINE + self.word))
            shortDudenLinks = soup.find_all('h3', text = self.word)
            # /rechtschreibung/vorantreiben -> vorantreiben
            self.displays = [link.a['href'].split('/')[-1] for link in shortDudenLinks]
        except:
            self.displays = []
            print 'Duden: word not found!'

    def getURLs(self):
        self.urls = [Duden.URLRECHTSCHREIBUNG + display for display in self.displays]
    
    def getDefinition(self, url):
        soup = BeautifulSoup(self.read(url))
        try:
            res = soup.find_all('span', 'helpref woerterbuch_hilfe_bedeutungen')
            # span (find_all) -> h2 (parent) -> ... (next sibling)
            html_result = res[-1].find_parent().find_next_sibling()
            definition = unicode(html_result).replace('\n', '')
        except:
            definition = ''
            print 'No definition found!'
        self.definitions.append(definition)

class Local:
    
    def __init__(self):
        try:
            self.godic = json.load(codecs.open(GODIC))
            self.duden = json.load(open(DUDEN))
        except:
            self.godic = {}
            self.duden = {}
        self.godic_left = []
        self.duden_left = []
    
    def update(self, wordList):
        count_godic = 0
        count_duden = 0
        for word in wordList:
            if word != '':
                # lookup in Godic
                if self.godic.has_key(word) == False:
                    dictest = Godic(word)
                    dictest.lookup()
                    if dictest.displays != []:
                        self.godic.update(dictest.createDictEntry())
                        count_godic += 1
                    else: self.godic_left.append(word)
                
                # lookup in Godic
                if self.duden.has_key(word) == False:
                    dictest = Duden(word)
                    dictest.lookup()
                    if dictest.displays != []:
                        self.duden.update(dictest.createDictEntry())
                        count_duden += 1
                    else: self.duden_left.append(word)
        
        print 'Godic updated:', count_godic
        print 'Duden update:', count_duden
    
    def save(self):
        # save dict locally
        json.dump(self.godic, open(GODIC, 'w'))
        json.dump(self.duden, open(DUDEN, 'w'))
        # save left word
        f_left = open('left.txt', 'w')
        f_left.write('Godic:\n\n')
        for word in self.godic_left:
            f_left.write(word + '\n')
        f_left.write('\n\nDuden:\n\n')
        for word in self.duden_left:
            f_left.write(word + '\n')
        f_left.close()
        print 'Godic count:', len(self.godic)
        print 'Duden count:', len(self.duden)
    
    def check(self, wordList):
        for word in wordList:
            if word == '':
                break
            if self.godic.has_key(word) == False:
                print 'Godic:', word
            if self.duden.has_key(word) == False:
                print 'Duden:', word