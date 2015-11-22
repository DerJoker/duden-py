# coding: UTF-8

'''
Created on Aug 2, 2015

@author: feng
'''

from bs4 import BeautifulSoup

class RechtschreibungHTML(object):

    def __init__(self, html):
        # complete link
        self.html = html.replace('href="/rechtschreibung/',
                                'href="http://www.duden.de/rechtschreibung/')
        self.soup = BeautifulSoup(self.html)
        self.sections = self.get_sections()
    
    def get_field_blaettern(self):
        return self.soup.find('div',class_='browse-lexem')
    
    def get_alphabet_davor(self):
        return self._get_alphabet('Im Alphabet davor')
    
    def get_alphabet_danach(self):
        return self._get_alphabet('Im Alphabet danach')
        
    def _get_alphabet(self, text):
        field_blaettern = self.get_field_blaettern()
        
        if field_blaettern != None:
            div = field_blaettern.find('div', class_='browse-lexem-title', text=text)
            # print next_div
            if div != None:
                next_lems = div.find_next_sibling()
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
    
    def get_wort_html(self):
        return unicode(self.soup.find('h1'))
    
    def get_wort_text(self):
        return unicode(self.soup.find('h1').get_text().strip())
    
    def get_sections(self):
        '''
        Sections:
            None
            <h2>Rechtschreibung</h2>
            <h2>Bedeutungsübersicht</h2>
            <h2>Wussten Sie schon?</h2>
            <h2>Synonyme zu <em>lassen</em></h2>
            <h2>Aussprache</h2>
            <h2>Herkunft</h2>
            <h2>Grammatik</h2>
            <h2>Typische Verbindungen</h2>
            <h2>Bedeutungen, Beispiele und Wendungen</h2>
            <h2>Blättern</h2>
        '''
        dict_sections = {}
        for section in self.soup.find_all('section'):
            dict_sections[unicode(section.find('h2'))] = section
        return dict_sections
    
    def get_section_aussprache(self):
        return self.sections.get(u'<h2>Aussprache</h2>', None)
    
    def get_sound_links(self):
        section_aussprache = self.get_section_aussprache()
        if section_aussprache != None:
            return [item['href'] for item in section_aussprache.find_all('a', class_='audio')]
        else: return []
        
    def get_section_bedeutungsuebersicht(self):
        return self.sections.get(u'<h2>Bedeutungsübersicht</h2>', None)
    
    def get_section_bedeutungen_beispiele_und_wendungen(self):
        return self.sections.get(u'<h2>Bedeutungen, Beispiele und Wendungen</h2>', None)
    
    def get_bedeutung_complete(self):
        res = {}
        
        section = self.get_section_bedeutungen_beispiele_und_wendungen()
        if section == None:
            section = self.get_section_bedeutungsuebersicht()
        
        '''
        <h3>Grammatik</h3>
        <h3>Aussprache</h3>
        <h3>Gebrauch</h3>
        <h3>Beispiel</h3>
        <h3>Beispiele</h3>
        <h3>Wendungen, Redensarten, Sprichwörter</h3>
        '''
        if section != None:
            tmp = {}
            for h3 in section.find_all('h3'):
                # key = definition with Grammatik, Beispiel etc.
                # value = list of options like Grammatik, Beispiel etc.
                tmp.setdefault(h3.parent.parent, []).append(h3)
            
            for key in tmp.keys():
                value = {}
                for item in tmp[key]:
                    # extract options, keep only definition as key
                    # value is also a dict (key = option, value = content)
                    value[unicode(item.extract())] = item.parent.extract()
                res[key] = value
        
        '''
        return empty list if neither above found, e.g. ausgleichbar
        '''
        return res
    
    def get_tuple_beispiel_bedeutung(self):
        res = []
        
        for (bedeutung, options) in self.get_bedeutung_complete().items():
            beispiele = options.get(u'<h3>Beispiele</h3>', None)
            # print beispiele
            beispiel = options.get(u'<h3>Beispiel</h3>', None)
            # print beispiel
            
            if beispiele != None:
                for li in beispiele.find_all('li'):
                    res.append((li,bedeutung))
                    
            if beispiel != None:
                res.append((beispiel,bedeutung))
        
        return res
        
def _unit_test_rechtschreibung():
    
    import sys
    sys.path.append('..')
    from tool import read
    url_read = read.read
    
    # test get_alphabet_davor(), get_alphabet_danach()
    lst_text = ['getrauen', 'a_italienische_Praeposition', 'a_Zeichen_fuer_und', 'd_Korrekturzeichen_fuer_tilgen',
                '80er_Jahre', '24_Sekunden_Regel']
    
    # test is_Wortschatz_des_Zertifikats_Deutsch()
    # lst_text = ['getrauen', 'lassen', 'nachdenken']
    
    # test bedeutung
    lst_text = ['getrauen', 'lassen', 'nachdenken', 'a_Zeichen_fuer_und', 'Abbild', 'abbilden', 'Abbildung', 
                'Abbruch', 'abbuegeln', 'abdecken', 'Abend', 'Abendbrot', 'Abendbrotzeit', 'abendessen', 
                'Abendessen', 'abendlich', 'Abendlicht', 'abends', 'Abenteuer', 'abenteuern', 
                'aber_Konjunktion_Bedeutung_doch', 'aber_Partikel', 'aber_Adverb_Bedeutung_wieder', 'aberglaeubig', 
                'abermalig', 'abermals', 'abfahren', 'abfahren_lassen', 'Ausgleich', 'ausgleichbar', 'ausgleichen', 
                'aushalten', 'Aushilfe', 'ausholen', 'auskaufen', 'Auskunft']
    
    for rechtschreibung in lst_text:
        print rechtschreibung
        html = url_read('http://www.duden.de/rechtschreibung/' + rechtschreibung)
        # print html
        rs = RechtschreibungHTML(html)
        # print rs.get_field_blaettern()
        # print rs.get_alphabet_davor()
        # print rs.get_alphabet_danach()
        # print rs.is_Wortschatz_des_Zertifikats_Deutsch()
        # print rs.get_wort_text()
        # print rs.get_sections()
        # print rs.get_sound_links()
        print rs.get_bedeutung_complete().items()
        print rs.get_tuple_beispiel_bedeutung()

if __name__ == '__main__':
    _unit_test_rechtschreibung()