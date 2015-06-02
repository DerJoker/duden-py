# coding: UTF-8

import random

import anki

from bs4 import BeautifulSoup
from duden import Rechtschreibung

'''
Function
'''

class Pronunciation:
    
    def __init__(self, html, rechtschreibung):
        self.html = html
        self.rechtschreibung = rechtschreibung
        self.links = {}
    
    def replace(self):
        '''
        self -> str
        
        Replace the following content (span) with Anki Sound Format [sound:(rechtschreibung)_IDxxx_xxx.mp3]
        
        <span class="audio" title="© Aussprachedatenbank der ARD">...</span>
        '''
        soup = BeautifulSoup(self.html)
        
        # <span class="audio" title="© Aussprachedatenbank der ARD"></span>
        for span in soup.find_all('span', class_='audio'):
            # mp3 link
            link = span.find('a', text='Als mp3 abspielen')['href']
            # local name
            text = self.rechtschreibung + '_' + link.split('/')[-1]
            # at the same time update mp3 links
            self.links[text] = link
            span.replace_with('[sound:' + text + ']')
        
        return unicode(soup)
    
    def getLinks(self):
        return self.links

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
    
    Return pure definitions.
    
    Arbeitnehmer
    <dd class="content">jemand, der von einem Arbeitgeber beschäftigt wird</dd>
    
    dadurch
    <li class="Bedeutung" id="Bedeutung1"> <span class="content"> da hindurch, durch diese Stelle, Öffnung hindurch</span> </li>
    <li class="Bedeutung"> <ol class="subterm_list"> <li id="Bedeutung2a"> <span class="content">durch dieses Mittel, Verfahren</span> </li> <li id="Bedeutung2b"> <span class="content">aus diesem Grund, durch diesen Umstand, auf diese Weise</span> </li> </ol> </li>
    
    ueberall
    <li id="Bedeutunga"> <span class="content">an jeder Stelle, an allen Orten; in jedem Bereich</span> </li>
    <li id="Bedeutungb"> <span class="content">bei jeder Gelegenheit</span> </li>
    
    Manager
    <li id="b2-Bedeutung-1"> <span class="content">mit weitgehender Verfügungsgewalt und Entscheidungsbefugnis ausgestattete, leitende Persönlichkeit eines Großunternehmens</span> </li>
    <li id="b2-Bedeutung-2"> <span class="content">geschäftlicher Betreuer von Künstlern, Berufssportlern o. Ä.</span> </li>
    '''
    def getDefinitions(self):
        rs_slice = Rechtschreibung(self.rechtschreibung).sliceBedeutungen()
        for df in rs_slice:
            soup = BeautifulSoup(df)
            
            # in case <li class="Bedeutung"> with sub term list
            dfs_contents = soup.select('li > ol > li')
            
            if dfs_contents == []:
                dfs_contents = soup.contents
            
            for item in dfs_contents:
                for h3 in item.find_all('h3'):
                    h3.parent.extract()
                
                if item.name in ['li', 'dd']:
                    item.name = 'div'
                
                print item
    
    '''
    -> [(str, str), ...]
    
    Return list of 2 strings (Tuple) as definition and examples    
    '''
    def getCardDefinitionWithExamples(self):
        results = []
        
        rs_slice = Rechtschreibung(self.rechtschreibung).sliceBedeutungen()
        for df in rs_slice:
            soup = BeautifulSoup(df)
            
            # in case <li class="Bedeutung"> with sub term list
            dfs_contents = soup.select('li > ol > li')
            
            if dfs_contents == []:
                dfs_contents = soup.contents
            
            for item in dfs_contents:
                beispiele = u''
                
                for h3 in item.find_all('h3'):
                    if h3.parent.has_attr('class') and h3.parent['class'] == [u'Beispiele']:
                        beispiele = h3.parent.extract()
                    else:
                        h3.parent.extract()
                
                if item.name in ['li', 'dd']:
                    item.name = 'div'
                
                results.append((unicode(item), unicode(beispiele)))
        
        return results
    
    '''
    -> [(str, str), ...]
    
    Return list of 2 strings (Tuple) as example and definition    
    '''
    def getCardExamples(self):
        results = []
        
        rs_slice = Rechtschreibung(self.rechtschreibung).sliceBedeutungen()
        for df in rs_slice:
            soup = BeautifulSoup(df)
            
            # in case <li class="Bedeutung"> with sub term list
            dfs_contents = soup.select('li > ol > li')
            
            if dfs_contents == []:
                dfs_contents = soup.contents
            
            for item in dfs_contents:
                beispiele = []
                
                for h3 in item.find_all('h3'):
                    if h3.parent.has_attr('class') and h3.parent['class'] == [u'Beispiele']:
                        beispiele = h3.parent.extract().find_all('span', class_='beispiel')
                    else:
                        h3.parent.extract()
                
                if item.name in ['li', 'dd']:
                    item.name = 'div'
                
                if beispiele != []:
                    results.extend([(unicode(beispiel), unicode(item)) for beispiel in beispiele])
        
        return results


'''
UnitTest
'''

if __name__ == '__main__':
    
#     f_anki_def = open('anki_definition_zd.txt', 'w')
    
    # Rechtschreibung list for test
    lt = [u'verheerend', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe', u'beobachten', u'modern_neu_modisch', u'schmuck', u'drauf', u'Anleitung']
    
    # WZD in wzd_list.txt
#     lt = [item.strip() for item in open('wzd_list.txt').readlines()]
    
    # special test cases of Sound
#     lt = [u'Aenderung', u'Aktivitaet', u'Anbieter', u'andere', u'Angestellter', u'ausreichend', u'Bedienungsanleitung', u'begeistert', u'Begruendung', u'Beratung', u'Bestaetigung', u'beste_Adjektiv', u'bestimmt_Adverb', u'Betreuung', u'Deutscher', u'Einfuehrung', u'Erhoehung', u'geboten_bieten', u'gestorben', u'Hersteller', u'interkulturell', u'Kindertagesstaette', u'langweilen', u'linke', u'Manager', u'maximal', u'naechste', u'Schlaf', u'Sekretaer', u'Traum_', u'vorige', u'aktiv', u'Alkohol', u'allerdings_Adverb', u'Artikel', u'Augenblick', u'augenblicklich', u'ausgezeichnet', u'benutzen', u'Cent', u'Chemie', u'dagegen', u'danach', u'darauf', u'darueber', u'deswegen', u'Dusche', u'Fleck', u'Geburt', u'gefallen_fallen', u'Geografie', u'gern', u'Hamburger_Speise_Gericht', u'Interesse', u'interessieren', u'Interview', u'Kilometer', u'Kredit_Finanzierung_Anleihe', u'Kritik', u'kritisch', u'Kurve', u'Langeweile', u'Motor', u'Motorrad', u'nachher', u'nutzen', u'passiv', u'Politik', u'Politiker', u'positiv', u'Scheck_Zahlungsanweisung_Bon', u'selbststaendig', u'Souvenir', u'Star_Kuenstler_Beruehmtheit', u'Stress', u'tatsaechlich_sicher_gewiss_garantiert', u'ueberall', u'unbedingt_zwingend', u'unheimlich', u'vorwaerts', u'Zentimeter', u'Arbeitnehmer', u'Balkon', u'Chance', u'dadurch', u'daher', u'darum', u'Mathematik', u'negativ', u'Saison', u'alltaeglich', u'Pension', u'Abteilung']
    
    random.shuffle(lt)
    
    for item in lt:
#         print item, ':', DudenFactory(item).getSoundText()
        print item
        word = Rechtschreibung(item).getWortText()
#         DudenFactory(item).getDefinitions()
        print DudenFactory(item).getCardExamples()
#         df = DudenFactory(item)
#         sound = df.getSoundText()
#         for (definition, examples) in df.getCardDefinitionWithExamples():
#             cd = anki.CardDefinition(word, definition, examples, sound)
#             f_anki_def.write(cd.makeCard())
#      
#     f_anki_def.close()
