# coding: UTF-8

'''
Created on Aug 2, 2015

@author: feng
'''

from bs4 import BeautifulSoup

class RechtschreibungHTML(object):
    '''
    classdocs
    '''

    def __init__(self, html):
        '''
        Constructor
        '''
        self.html = html.replace('href="/rechtschreibung/',
                                    'href="http://www.duden.de/rechtschreibung/')
        self.soup = BeautifulSoup(self.html)
        self.links = {}    # dict {text:link, ...}
    
    def get_field_blaettern(self):
        return self.soup.find('div',class_='browse-lexem')
    
    def get_alphabet_davor(self):
        field_blaettern = self.get_field_blaettern()
        
        if field_blaettern != None:
            prev_div = field_blaettern.find('div', class_='browse-lexem-title', text='Im Alphabet davor')
#             print prev_div
            if prev_div != None:
                prev_lems = prev_div.find_next_sibling()
                return [(a.get_text(), a['href'].split('/')[-1]) for a in prev_lems.find_all('a')]
            else: return []
        
        return []
    
    def get_alphabet_danach(self):
        field_blaettern = self.get_field_blaettern()
        
        if field_blaettern != None:
            next_div = field_blaettern.find('div', class_='browse-lexem-title', text='Im Alphabet danach')
#             print next_div
            if next_div != None:
                next_lems = next_div.find_next_sibling()
                return [(a.get_text(), a['href'].split('/')[-1]) for a in next_lems.find_all('a')]
            else: return []
        
        return []
    
    def is_Wortschatz_des_Zertifikats_Deutsch(self):
        # example: nachdenken
        # Dieses Wort stand 1961 erstmals im Rechtschreibduden.
        # Dieses Wort gehört zum Wortschatz des Zertifikats Deutsch.
        div_entries = self.soup.find_all('div',class_='entry')
        for item in div_entries:
            if u'Dieses Wort gehört zum Wortschatz des Zertifikats Deutsch.' in item.get_text():
                return True
        return False
        
def _unit_test_rechtschreibung():
    
    import sys
    sys.path.append('..')
    from tool import read
    url_read = read.read
    
    # test get_alphabet_davor(), get_alphabet_danach()
    lst_text = ['getrauen', 'a_italienische_Praeposition', 'a_Zeichen_fuer_und', 'd_Korrekturzeichen_fuer_tilgen',
                '80er_Jahre', '24_Sekunden_Regel']
    
    # test is_Wortschatz_des_Zertifikats_Deutsch()
#     lst_text = ['getrauen', 'lassen', 'nachdenken']
    
    for rechtschreibung in lst_text:
        print rechtschreibung
        html = url_read('http://www.duden.de/rechtschreibung/' + rechtschreibung)
#         print html
        rs = RechtschreibungHTML(html)
#         print rs.get_field_blaettern()
        print rs.get_alphabet_davor()
        print rs.get_alphabet_danach()
        print rs.is_Wortschatz_des_Zertifikats_Deutsch()

if __name__ == '__main__':
    _unit_test_rechtschreibung()