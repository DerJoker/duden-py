# coding: UTF-8

from bs4 import BeautifulSoup

import tools

'''
Class
'''

class Duden:
    
    def __init__(self):
        print 'Duden'

class Rechtschreibung:
    
    URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'
    
    def __init__(self, d_rechtschreibung):
        self.rechtschreibung = d_rechtschreibung
        self.url = Rechtschreibung.URLRECHTSCHREIBUNG + d_rechtschreibung
        
        self.html = tools.read(self.url)
        
        self.soup = BeautifulSoup(self.html)
    
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
        return unicode(self.soup.find('div', class_='field-name-field-pronunciation'))
    
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
    def getTupleExampleAndDefinition(self):
        results = []
        
        rs_slice = self.sliceBedeutungen()
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
#     f_log = open('log.txt','w')
    
    # Rechtschreibung list for test
    lt = [u'Chip', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe', u'beobachten', \
          u'modern_neu_modisch', u'schmuck', u'drauf', u'Anleitung']
    
    for item in lt:
        rs = Rechtschreibung(item)
        
        print item, ':', rs.getWortText()
        print rs.getTupleExampleAndDefinition()