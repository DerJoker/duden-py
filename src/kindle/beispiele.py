# coding: UTF-8

import urllib
import urllib2
from bs4 import BeautifulSoup

"""
Configuration
"""

# mp3 download path
_path_duden_mp3 = '../mp3/'

"""
Q:
beispiel
A:
[sound]
wort : bedeutung
"""

URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'

def read(url):
    TIMEOUT = 60
    TRY = 10
    count = 0
    r = ''
    while (count < TRY and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=TIMEOUT).read()
        except Exception,e:
            print e
            r = ''
        count += 1
    return r

class Rechtschreibung:
    
    # access key
    k_word = 'word'
    k_pron = 'pronunciation'
    k_extra = 'extra'
    
    def __init__(self, d_rechtschreibung):
        if self.isValid(d_rechtschreibung):
            self.rechtschreibung = d_rechtschreibung
            self.url = URLRECHTSCHREIBUNG + d_rechtschreibung
            
            self.soup = BeautifulSoup(read(self.url))
            
            self.wort = self.soup.select('h1 span span')[0].get_text()
            
            self.misc = ''  # Grammatik, Gebrauch
            self.bedeutungen = []
            self.content = self.getContent()
            print 'init Wort.'
        else:
            print 'Rechtschreibung invlaid:', d_rechtschreibung
    
    def isValid(self, d_rechtschreibung):
        return True
    
    def downloadMP3(self):
        try:
            # it could happen that, there's no mp3 (e.g. sicher_machen)
            url_mp3 = self.soup.find('a', text="Als mp3 abspielen")['href']
            local_mp3 = _path_duden_mp3 + self.rechtschreibung + '.mp3'
            urllib.urlretrieve(url_mp3, local_mp3)
            self.content[Rechtschreibung.k_pron] = self.rechtschreibung + '.mp3'
            print 'mp3 downloaded.'
        except Exception,e:
            print e
            
    def getRechtschreibungOnPage(self):
        return [link['href'].split('/')[-1] for link in self.soup.select('a[href^="/rechtschreibung/"]')]
    
    '''
    {'word':'sicher','pronunciation':'[sound:sicher.mp3]',
    'extra':[{
    'definition':'d1',
    'picture':None,
    'examples':[],
    'idioms':[],
    'misc':'Grammatik, Gebrauch, Herkunft ...'
    }, ...
    ]}
    '''
    def getContent(self):
        content = {Rechtschreibung.k_word:self.wort, Rechtschreibung.k_pron:None, Rechtschreibung.k_extra:[]}
        
        # Bedeutungen, Beispiele und Wendungen
        bbw = self.soup.find('div', class_='field-name-field-examples')
        if bbw.get_text() != '':
            for li in bbw.select('ol > li'):
                try:
                    divs = li.span.div.extract()
                except Exception,e:
                    print e
                    divs = []
                print divs
                content[Rechtschreibung.k_extra].append(li.span)
            return content
        
        # Bedeutung
        b = self.soup.find('div', class_='field-name-field-abstract')
        if b.get_text() != '':
            return content
        
        return content