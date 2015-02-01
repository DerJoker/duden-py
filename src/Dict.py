#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup

# define CONSTANT

CODEC = 'utf-8'

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

