# coding: UTF-8

import urllib2
import shelve
from bs4 import BeautifulSoup

# define CONSTANT

CODEC = 'UTF-8'

GODIC = 'godicdb'
DUDEN = 'dudendb'

GODICDB = 'godicdb'
DUDENDB = 'dudendb'

CLASSREFLINK = 'reflink'
CLASSDUDEN = 'duden'
CLASSGODIC = 'godic'

DEFINITION = {'display': '', 'url': '', 'content': ''}

TIMEOUT = 60

def makeHyperlink(display, link):
    return '<div><a href="' + link + '">' + display + '</a></div>\n'

def makeDiv(class_, divin):
    return '<div class="' + class_ + '">' + divin + '</div>'

class DictEntry:
    
    def __init__(self, word):
        self.word = word.strip()
#         self.word = word.encode(CODEC)
        self.definitions = []   # DEFINITION
    
    def read(self, url):
        url = url.encode(CODEC)
        try:
            return urllib2.urlopen(url, timeout=TIMEOUT).read()
        except:
            return ''
            print '(Timeout) Failed to load', url
    
    def isValid(self):
        if self.word == '' or self.definitions == []:
            return False
        else: return True

class Godic(DictEntry):
    
    URLGODIC = u'http://www.godic.net/dicts/de/'
    
    def getDefinition(self, url):
        soup = BeautifulSoup(self.read(url))
        res = soup.find('div', id='tabs--11')  # type <class 'bs4.element.Tag'>
#         try:
#             res.a.decompose()
#         except:
#             print 'Exception a.decompose()'
        # if res = None, definition = 'None'
        definition = str(res).replace('\n', '')
        return definition # Worst situation: 'None'
    
    def lookup(self):
        godicDefinition = DEFINITION.copy()
        godicDefinition['display'] = self.word
        godicDefinition['url'] = Godic.URLGODIC + godicDefinition['display']
        godicDefinition['content'] = self.getDefinition(godicDefinition['url'])
        self.definitions.append(godicDefinition)

class Duden(DictEntry):
    
    URLRECHTSCHREIBUNG = u'http://www.duden.de/rechtschreibung/'
    URLDUDENONLINE = u'http://www.duden.de/suchen/dudenonline/'
    
    def getDisplays(self):
        soup = BeautifulSoup(self.read(Duden.URLDUDENONLINE + self.word))
        shortDudenLinks = soup.find_all('h3', text = self.word.encode(CODEC))
        if shortDudenLinks != []:
            for link in shortDudenLinks:
                dudenDefinition = DEFINITION.copy()
                # /rechtschreibung/vorantreiben -> vorantreiben
                dudenDefinition['display'] = link.a['href'].split('/')[-1]
                dudenDefinition['url'] = Duden.URLRECHTSCHREIBUNG + dudenDefinition['display'].decode(CODEC)
                self.definitions.append(dudenDefinition)
        else: print 'Exception:', self.word, 'not found in Duden!'
    
    def getDefinition(self, url):
        soup = BeautifulSoup(self.read(url))
        res = soup.find_all('span', 'helpref woerterbuch_hilfe_bedeutungen')
        print 'len res:', len(res)
        try:
            # span (find_all) -> h2 (parent) -> ... (next sibling)
            html_result = res[-1].find_parent().find_next_sibling()
            definition = unicode(html_result).replace('\n', '')
        except:
            definition = ''
            print 'No definition found in Duden!'
            print 'url: ', url
        return definition
    
    def lookup(self):
        self.getDisplays()
        for definition in self.definitions:
            definition['content'] = self.getDefinition(definition['url'])
    
    def printDefinitions(self):
        s = ''
        for item in self.definitions:
            s += makeHyperlink(item['display'], item['url'])
            s += item['content']
        print makeDiv(CLASSDUDEN, s)
    
    def printReflink(self):
        s = ''
        for item in self.definitions:
            s += makeHyperlink(item['display'], item['url'])
        return makeDiv(CLASSREFLINK, s)

class Local:
    
    def __init__(self):
        self.godic = shelve.open(GODICDB)
        self.duden = shelve.open(DUDENDB)
    
    def addEntry(self, word):
        if word != '':
            # lookup in Godic
            if self.godic.has_key(word.encode(CODEC)) == False:
                dictgodic = Godic(word)
                dictgodic.lookup()
                if dictgodic.isValid():
                    self.godic[word.encode(CODEC)] = dictgodic.definitions
#                     self.godic[word.encode(CODEC)] = 'dictgodic.definitions'
                else: print word, 'not valid in Godic!'
            
            # lookup in Godic
            if self.duden.has_key(word.encode(CODEC)) == False:
                dictduden = Duden(word)
                dictduden.lookup()
                if dictduden.isValid():
                    self.duden[word.encode(CODEC)] = dictduden.definitions
                else: print word, 'not valid in Duden!'
    
    def save(self):
        self.godic.close()
        self.duden.close()
    
    def check(self, wordList):
        for word in wordList:
            if word == '':
                break
            if self.godic.has_key(word) == False:
                print 'Godic:', word
            if self.duden.has_key(word) == False:
                print 'Duden:', word