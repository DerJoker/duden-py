# coding: UTF-8

import urllib
import urllib2
from bs4 import BeautifulSoup

from Anki import CardImg
from Anki import CardIdiom
from Anki import CardExample

"""
Configuration
"""

# sound download path
_path_duden_mp3 = '../mp3/'
# picture download path
_path_duden_img = '../img/'

'''
Constant
'''

CODEC = 'UTF-8'

'''
Function
'''

# #Improve#

def read(url):
    TIMEOUT = 60
    TRY = 5
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

'''
Class
'''

class Rechtschreibung:
    
    URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'
    
    # access key
    k_img = 'img'
    k_text = 'text'
    k_def = 'definition'
    k_examples = 'examples'
    
    def __init__(self, d_rechtschreibung):
        self.rechtschreibung = d_rechtschreibung
        self.url = Rechtschreibung.URLRECHTSCHREIBUNG + d_rechtschreibung
        
        self.html = read(self.url).replace('\n', '')    # no newline, prepare for Anki card
        self.soup = BeautifulSoup(self.html)
        
        self.wort = self.soup.select('h1 span span')[0].get_text()
        
        self.aussprache = ''
        
        self.bild = []
    
    def downloadMP3(self):
        try:
            # it could happen that, there's no mp3 (e.g. sicher_machen)
            url_mp3 = self.soup.find('a', text="Als mp3 abspielen")['href']
            self.aussprache = self.rechtschreibung + '.mp3'
        except Exception,e:
            print e
        
        if self.aussprache != '':
            local_mp3 = _path_duden_mp3 + self.aussprache
            urllib.urlretrieve(url_mp3, local_mp3)
            print 'mp3 downloaded.'
    
    def printAnkiAussprache(self):
        if self.aussprache != '':
            return '<br>[sound:' + self.aussprache + ']'
        else: return ''
    
    def downloadImg(self):
        imgs = self.soup.find_all('img', class_='hidden')
        
        for index in range(len(imgs)):
            text = str(imgs[index].find_next_sibling('span', class_='bu')).decode(CODEC)
            
            url_img = imgs[index]['src']
            img_name = self.rechtschreibung + '-' + str(index) + '.' + url_img.split('.')[-1]
            local_img = _path_duden_img + img_name
            urllib.urlretrieve(url_img, local_img)
            print 'Image downloaded.'
            
            content = BeautifulSoup(str(imgs[index].find_parent('span', class_='content')))
            for div in content.find_all(['div', 'span'],recursive=False):
                div.decompose()
            definition = str(content).decode(CODEC)
                        
            self.bild.append({Rechtschreibung.k_img:img_name, Rechtschreibung.k_text:text, Rechtschreibung.k_def:definition})
    
    def getBeispiele(self):
        b = []
        
        beispiele = self.soup.find_all('div', class_='Beispiele')
        
        for beispiel in beispiele:
            bedeutung = BeautifulSoup(str(beispiel.parent))
            for div in bedeutung.find_all('div'):
                div.decompose()
            examples = []
            for bs in beispiel.find_all('span', class_='beispiel'):
                examples.append(str(bs).decode(CODEC))
            b.append({Rechtschreibung.k_def:str(bedeutung).decode(CODEC),Rechtschreibung.k_examples:examples})
        
        return b
    
    def printAnkiBeispiel(self):
        str_anki = ''
        for item in self.getBeispiele():
            for example in item[Rechtschreibung.k_examples]:
                str_anki += example.replace('\n', '') + '\t' + self.wort + ' : ' + item[Rechtschreibung.k_def].replace('\n', '')
                str_anki += self.printAnkiAussprache()
                str_anki += '\n\n'
        return str_anki.encode('utf-8')
    
    def getWendungen(self):
        print 'Wendungen'
    
    # return Recthschreibung on page without Blaettern part
    def getRechtschreibungOnPage(self):
        soup = BeautifulSoup(self.html)
        # remove Blaettern part (Im Alphabet davor, Im Alphabet danach)
        soup.find('div', class_='field-name-field-browse').extract()
        # /rechtschreibung/fallen#b2-Bedeutung-1d -> fallen
        return [link['href'].split('/')[-1].split('#')[0] for link in soup.select('a[href^="/rechtschreibung/"]')]
