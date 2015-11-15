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

from alphabetcsv import AlphabetCSV
from downloadlog import DownloadLogEntryFactory, DownloadLog

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

    def _get_aussprache(self):
        '''
        get anki sound text (private)
        '''
        aussprache = self.rshtml.get_section_aussprache()
        if aussprache != None:
            aussprache = self._handle_sound_text(aussprache)
        else: aussprache = ''
        return aussprache

    def get_card_aussprache(self):
        '''
        return tuple (wort as front, aussprache as back)
        '''
        wort = self.rshtml.get_wort_text()
        aussprache = self._get_aussprache()
        return (wort, unicode(aussprache))
    
    def get_card_examples(self):
        '''
        return list of (example as front, definition as back)
        '''
        res = []
        aussprache = self._get_aussprache()
        
        for (beispiel, bedeutung) in self.get_tuple_beispiel_bedeutung():
            front = '<div class="' + self.wort_rs + '"></div>' + unicode(beispiel)
            # bedeutung = self._handle_image_text(bedeutung)
            
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

'''
Main
'''

def make_cards_aussprache():
    fieldname_aussprache = 'aussprache'
    fn_anki_result_csv = 'anki.' + fieldname_aussprache + '.csv'

    alphabetcsv = AlphabetCSV(fieldname_aussprache)

    with open(fn_anki_result_csv, 'w') as csv_anki_result:
        writer = csv.writer(csv_anki_result)
        for item in alphabetcsv.getNoneEmptyList():
            print item
            html = read_from_local(item + '.html')
            print html
            anki = Anki(item, html)
            writer.writerow(anki.get_card_aussprache())

if __name__ == '__main__':
    make_cards_aussprache()