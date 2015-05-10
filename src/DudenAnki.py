# coding: UTF-8

import anki

from bs4 import BeautifulSoup
from duden import Rechtschreibung

class DudenFactory:
    
    def __init__(self, rechtschreibung):
        self.rechtschreibung = rechtschreibung
        self.mp3Links = []
    
    '''
    str -> str
    (rechtschreibung slice -> text)
    
    Return text with Anki Sound Format [sound:(rechtschreibung)_ID....mp3]. Replaced respectively in special cases like # Case 5, e.g. Abteilung.
    
    Aussprache / Pronunciation:
    
    # Case 1: normal (1) pronunciation
    
    verheerend
    
    Betonung:
        verhe̲e̲rend
    
    # Case 2: no mp3
    
    Angestellter
    
    Betonung:
        Ạngestellter 
    Lautschrift:
        [ˈanɡəʃtɛltɐ] 
    
    # Case 3: different writings, different pronunciations
    
    selbststaendig
    
    Betonung:
        sẹlbstständig 
        sẹlbständig
    
    # Case 4: more (1+) pronunciations (regional / dialect)
    
    Pension
    
    Lautschrift:
        [pãˈzi̯oːn]  , [paŋ…]  , besonders süddeutsch, österreichisch, schweizerisch: [pɛn…]  , besonders schweizerisch auch: [pãˈsi̯oːn]
    
    Chance
    
    Lautschrift:
        [ˈʃãːs(ə)]  , auch: [ˈʃaŋsə] 
    
    # Case 5: different meanings, different pronunciations
    
    Abteilung
    
    Lautschrift:
        [apˈta͜ilʊŋ] 
    
    '''
    def getSoundText(self):
        rs_slice = Rechtschreibung(self.rechtschreibung).sliceAussprache()
        soup = BeautifulSoup(rs_slice)
        
        # <span class="audio" title="© Aussprachedatenbank der ARD"></span>
        for span in soup.find_all('span', class_='audio'):
            mp3_link = span.find('a', text='Als mp3 abspielen')['href']
            # at the same time add to list (mp3Links)
            self.mp3Links.append(mp3_link)
            span.replace_with('[sound:' + self.rechtschreibung + '_' + mp3_link.split('/')[-1] + ']')
        
        return unicode(soup.find('dl'))


'''
UnitTest
'''

if __name__ == '__main__':
    
    # Rechtschreibung list for test
    lt = [u'verhe̲e̲rend', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe', u'beobachten', u'modern_neu_modisch', u'schmuck', u'drauf', u'Anleitung']
    
    # WZD in wzd_list.txt
#     lt = [item.strip() for item in open('wzd_list.txt').readlines()]
    
    # special test cases of Sound
    lt = [u'Aenderung', u'Aktivitaet', u'Anbieter', u'andere', u'Angestellter', u'ausreichend', u'Bedienungsanleitung', u'begeistert', u'Begruendung', u'Beratung', u'Bestaetigung', u'beste_Adjektiv', u'bestimmt_Adverb', u'Betreuung', u'Deutscher', u'Einfuehrung', u'Erhoehung', u'geboten_bieten', u'gestorben', u'Hersteller', u'interkulturell', u'Kindertagesstaette', u'langweilen', u'linke', u'Manager', u'maximal', u'naechste', u'Schlaf', u'Sekretaer', u'Traum_', u'vorige', u'aktiv', u'Alkohol', u'allerdings_Adverb', u'Artikel', u'Augenblick', u'augenblicklich', u'ausgezeichnet', u'benutzen', u'Cent', u'Chemie', u'dagegen', u'danach', u'darauf', u'darueber', u'deswegen', u'Dusche', u'Fleck', u'Geburt', u'gefallen_fallen', u'Geografie', u'gern', u'Hamburger_Speise_Gericht', u'Interesse', u'interessieren', u'Interview', u'Kilometer', u'Kredit_Finanzierung_Anleihe', u'Kritik', u'kritisch', u'Kurve', u'Langeweile', u'Motor', u'Motorrad', u'nachher', u'nutzen', u'passiv', u'Politik', u'Politiker', u'positiv', u'Scheck_Zahlungsanweisung_Bon', u'selbststaendig', u'Souvenir', u'Star_Kuenstler_Beruehmtheit', u'Stress', u'tatsaechlich_sicher_gewiss_garantiert', u'ueberall', u'unbedingt_zwingend', u'unheimlich', u'vorwaerts', u'Zentimeter', u'Arbeitnehmer', u'Balkon', u'Chance', u'dadurch', u'daher', u'darum', u'Mathematik', u'negativ', u'Saison', u'alltaeglich', u'Pension', u'Abteilung']
    
    for item in lt:
        print item, ':', DudenFactory(item).getSoundText()
