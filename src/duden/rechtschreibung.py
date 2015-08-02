'''
Created on Aug 2, 2015

@author: feng
'''

from bs4 import BeautifulSoup

import sys
sys.path.append('..')
from tool import read
read_url = read.read

class Rechtschreibung(object):
    '''
    classdocs
    '''
    
    URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'

    def __init__(self, rechtschreibung):
        '''
        Constructor
        '''
        self.rechtschreibung = rechtschreibung
        
        self.url = Rechtschreibung.URLRECHTSCHREIBUNG + rechtschreibung
        self.html = read_url(self.url).replace('href="/rechtschreibung/',
                                           'href="http://www.duden.de/rechtschreibung/')
        self.soup = BeautifulSoup(self.html)
        self.links = {}    # dict {text:link, ...}
    
    def get_field_blaettern(self):
        return self.soup.find('div',class_='field-name-field-browse')
    
    def get_alphabet_davor(self):
        field_blaettern = self.get_field_blaettern()
        
        if field_blaettern != None:
            prev_lems = field_blaettern.find('span', class_='prev_lems')
            if prev_lems != None:
                return [(a.get_text(), a['href'].split('/')[-1]) for a in prev_lems.find_all('a')]
            else: return []
        
        return []
    
    def get_alphabet_danach(self):
        field_blaettern = self.get_field_blaettern()
        
        if field_blaettern != None:
            next_lems = field_blaettern.find('span', class_='next_lems')
            if next_lems != None:
                return [(a.get_text(), a['href'].split('/')[-1]) for a in next_lems.find_all('a')]
            else: return []
        
        return []
        
def _unit_test_rechtschreibung():
    lst_text = ['getrauen', 'a_italienische_Praeposition', 'a_Zeichen_fuer_und', 'd_Korrekturzeichen_fuer_tilgen']
    
    for rechtschreibung in lst_text:
        rs = Rechtschreibung(rechtschreibung)
#         print rs.get_field_blaettern()
        print rs.get_alphabet_davor()

if __name__ == '__main__':
    _unit_test_rechtschreibung()