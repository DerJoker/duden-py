# coding: UTF-8

import logging

from bs4 import BeautifulSoup

import tools

'''
Class
'''

class Duden:
    
    URLDUDENONLINE = 'http://www.duden.de/suchen/dudenonline/'
    
    def __init__(self, wort):
        self.wort = wort
        self.url = Duden.URLDUDENONLINE + wort
    
    def getRechtschreibung(self):
        '''
        Return list of Rechtschreibung, which (exactly) equals to the search word
        
        self -> [rechtschreibung, ...]
        '''
        html = tools.read(self.url)
        soup = BeautifulSoup(html)
#         return [item.text for item in soup.find_all('h3')]
        return [item['href'].split('/')[-1] for item in soup.find_all('a', text=self.wort.decode('utf-8'))]

class Rechtschreibung:
    
    URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'
    
    def __init__(self, d_rechtschreibung):
        self.rechtschreibung = d_rechtschreibung
        self.url = Rechtschreibung.URLRECHTSCHREIBUNG + d_rechtschreibung
        
        self.html = tools.read(self.url).replace('href="/rechtschreibung/', 
                                                 'href="http://www.duden.de/rechtschreibung/')
        
        self.soup = BeautifulSoup(self.html)
        
        self.links = {}    # dict {text:link, ...}
    
    '''
    -> str (unicode)
    
    Return word
    '''
    def getWortHTML(self):
        return unicode(self.soup.find('h1'))
    
    def getWortText(self):
        return unicode(self.soup.find('h1').get_text().strip())
    
    '''
    -> str (unicode)
    
    Return slice Aussprache.
    '''
    def sliceAussprache(self):
        return unicode(self.soup.find('div', class_='field-name-field-pronunciation').find('dl'))
    
    def getSoundLinks(self):
        soup = BeautifulSoup(self.sliceAussprache())
        return [item['href'] for item in soup.find_all('a', text='Als mp3 abspielen')]
    
    '''
    -> str (unicode)
    
    Return anki sound.
    '''
    def getAnkiSound(self):
        return self.__handleSoundText(self.sliceAussprache())
    
    '''
    -> [str]
    
    Return list of Bedeutungen / definitions with examples, if there is.
    
    Besides Bedeutung / definition, there can also be (class name):
     + Abkuerzung
     + Aussprache
     + Besonderheiten
     + Beispiele
     + Grammatik
     + Herkunft
     + Wendungen
     + Gebrauch
    
    Among which, what could be of interest are Beispiele and Wendungen.
    '''
    def sliceBedeutungen(self):
        # try first field examples
        field_examples = self.soup.find('div',class_='field-name-field-examples')
        
        if field_examples != None and field_examples.find('h2') != None:
            return [unicode(item) for item in field_examples.find('h2').find_next_sibling().find_all(recursive=False)]
        
        # if not, try then field abstract
        field_abstract = self.soup.find('div',class_='field-name-field-abstract')
        
        if field_abstract != None and field_abstract.find('h2') != None:
            return [unicode(item) for item in field_abstract.find('h2').find_next_sibling().find_all(recursive=False)]
        
        # it shouldn't come to this ...
        return []
    
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
        rs_slice = self.sliceBedeutungen()
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
    def getTupleDefinitionAndExamples(self):
        results = []
        
        rs_slice = self.sliceBedeutungen()
        for df in rs_slice:
            soup = BeautifulSoup(df)
            
            # in case <li class="Bedeutung"> with sub term list
            dfs_contents = soup.select('li > ol > li')
            
            if dfs_contents == []:
                dfs_contents = soup.contents
            
            for item in dfs_contents:
                beispiele = u''
                
                for h3 in item.find_all('h3'):
                    if h3.parent.has_attr('class'):
                        if h3.parent['class'] == [u'Beispiele']:
                            beispiele = h3.parent.extract()
                        # keep Aussprache and Grammatik
                        elif h3.parent['class'] not in [[u'Aussprache'], [u'Grammatik']]:
                            h3.parent.extract()
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
    def getTupleExampleAndDefinition(self):
        res = []
        
        for (deinition, examples) in self.getTupleDefinitionAndExamples():
            for beispiel in BeautifulSoup(examples).find_all('span', class_='beispiel'):
                res.append((unicode(beispiel), unicode(deinition)))
        
        return res
    
    def __handleSoundText(self, text):
        '''
        handle sound text (duden html -> anki)
        
        e.g.
        ...
        <span class="audio" title="© Aussprachedatenbank der ARD">
            ...
            <a target="_blank" title="Als mp3 abspielen - © Aussprachedatenbank der ARD" 
            href="http://www.duden.de/_media_/audio/ID4116703_498035746.mp3">Als mp3 abspielen</a>
            ...
        </span>
        ...
        ->
        ...
        [sound:ID4116703_498035746.mp3]
        ...
        '''
        soup = BeautifulSoup(text)
        
        # <span class="audio" title="© Aussprachedatenbank der ARD"></span>
        for span in soup.find_all('span', class_='audio'):
            mp3_link = span.find('a', text='Als mp3 abspielen')['href']
            # at the same time add link to dict links
            self.links[mp3_link.split('/')[-1]] = mp3_link
            span.string = '[sound:' + mp3_link.split('/')[-1] + ']'
            del span['title']
            del span['class']
        
        return unicode(soup)


'''
UnitTest
'''

def __UnitTest_Duden():
    
    '''
    stän­dig: in last page of the result -> go throught all pages
    '''
    lt_wort = ['Abteilung', 'Magen', 'stän­dig', 'vollständig', 'Maß', 'dauern', 'behandln', 'aufweisen']
    
    for item in lt_wort:
        duden = Duden(item)
        print item
        print duden.getRechtschreibung()

def __UnitTest_Rechtschreibung():
    
    # Rechtschreibung list for test
    lt = [u'Chip', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe']
    
    for item in lt:
        rs = Rechtschreibung(item)
        
        print item, ':', rs.getWortText()
        print rs.getAnkiSound()
        print rs.getTupleExampleAndDefinition()

if __name__ == '__main__':
    
#     __UnitTest_Duden()
    __UnitTest_Rechtschreibung()