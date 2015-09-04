# coding: UTF-8

'''
Created on Sep 2, 2015

@author: feng
'''

import csv

from bs4 import BeautifulSoup

from rechtschreibung import RechtschreibungHTML
import local
read_from_local = local.read_from_local
save_media = local.save_media

class Anki():
    
    def __init__(self, wort_rs, html):
        self.wort_rs = wort_rs
        self.rshtml = RechtschreibungHTML(html)
        self.links = {}    # dict {text:link, ...}
    
    def get_tuple_beispiel_bedeutung(self):
        res = []
        
        for (bedeutung, options) in self.rshtml.get_bedeutung_complete().items():
            bedeutung = self._handle_image_text(bedeutung)
            
            beispiele = options.get(u'<h3>Beispiele</h3>', None)
#             print beispiele
            beispiel = options.get(u'<h3>Beispiel</h3>', None)
#             print beispiel
            
            if beispiele != None:
                for li in beispiele.find_all('li'):
                    res.append((li,bedeutung))
                    
            if beispiel != None:
                res.append((beispiel,bedeutung))
        
        return res
    
    def get_card_examples(self):
        '''
        return list of (example as front, definition as back)
        '''
        res = []
        aussprache = self.rshtml.get_section_aussprache()
        if aussprache != None:
            aussprache = self._handle_sound_text(aussprache)
        else: aussprache = ''
        
        for (beispiel, bedeutung) in self.get_tuple_beispiel_bedeutung():
            front = '<div class="' + self.wort_rs + '"></div>' + unicode(beispiel)
#             bedeutung = self._handle_image_text(bedeutung)
            
            back = self.rshtml.get_wort_text() + ' : ' + unicode(bedeutung) + '<br >' + unicode(aussprache)
            res.append((front, back))
        
        return res
    
    def _handle_image_text(self, nvstring):
        if nvstring == None:
            return nvstring
        
        soup = BeautifulSoup()
        for figure in nvstring.find_all('figure'):
            src = figure.find('img')['src']
            src_local = src.split('/')[-1]
            self.links[src_local] = src
            img = soup.new_tag('img')
            img['src'] = src_local
            figure.img.replace_with(img)
        
        return nvstring
    
    def _handle_sound_text(self, nvstring):
        if nvstring == None:
            return nvstring
        
        soup = BeautifulSoup()
        for audio in nvstring.find_all('a', class_='audio'):
            href = audio['href']
            href_local = self.wort_rs + '-' + href.split('/')[-1]
            self.links[href_local] = href
            span = soup.new_tag('span')
            span.string = '[sound:' + href_local + ']'
            audio.replace_with(span)
        
        return nvstring

def _unit_test_anki():
    import sys
    sys.path.append('..')
    from tool import read
    url_read = read.read
    
    lst_text = ['getrauen', 'lassen', 'nachdenken', 'a_Zeichen_fuer_und', 'Abbild', 'abbilden', 'Abbildung', 
                'Abbruch', 'abbuegeln', 'abdecken', 'Abend', 'Abendbrot', 'Abendbrotzeit', 'abendessen', 
                'Abendessen', 'abendlich', 'Abendlicht', 'abends', 'Abenteuer', 'abenteuern', 
                'aber_Konjunktion_Bedeutung_doch', 'aber_Partikel', 'aber_Adverb_Bedeutung_wieder', 'aberglaeubig', 
                'abermalig', 'abermals', 'abfahren', 'abfahren_lassen', 'Ausgleich', 'ausgleichbar', 'ausgleichen', 
                'aushalten', 'Aushilfe', 'ausholen', 'auskaufen', 'Auskunft']
    
    lst_text = ['Abfahrt', 'Abfall', 'Abnormitaet']
    
    for rechtschreibung in lst_text:
        html = url_read('http://www.duden.de/rechtschreibung/' + rechtschreibung)
        anki = Anki(rechtschreibung, html)
#         print anki.get_tuple_beispiel_bedeutung()
        for (front, back) in anki.get_card_examples():
            print front + '\t' + back
        print anki.links

def make_cards_exmaple():
    
    # read from 'alphabet.edit.csv'
    fn_alphabet_edit_csv = 'alphabet.edit.csv'
    # write into 'anki.result.csv'
    fn_anki_result_csv = 'anki.result.csv'
    
    with open(fn_anki_result_csv, 'w') as csv_anki_result:
        pass
    
    with open(fn_alphabet_edit_csv) as csv_alphabet_edit:
        reader = csv.DictReader(csv_alphabet_edit)
        for row in reader:
            if row['star'] != '':
                wort_rs = row['rechtschreibung']
                print wort_rs
                html = read_from_local(wort_rs + '.html')
                 
                anki = Anki(wort_rs, html)
                 
                with open(fn_anki_result_csv, 'a') as csv_anki_result:
                    writer = csv.writer(csv_anki_result)
                    writer.writerows([(front.encode('utf-8'), back.encode('utf-8'))
                                      for (front, back) in anki.get_card_examples()])
                     
                for (key, value) in anki.links.items():
                    if save_media(value, key) != True:
                        print 'download failed:', key, value

if __name__ == '__main__':
#     _unit_test_anki()
    
    make_cards_exmaple()