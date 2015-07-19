# coding: UTF-8

from bs4 import BeautifulSoup

from duden import Rechtschreibung

class AnkiRechtschreibung(Rechtschreibung):
    
    __links = {}    # dict {text:link, ...} (mp3, jpg etc.)
    
    def getLinks(self):
        return self.__links
    
    def _handleSoundText(self, text):
        '''
        handle sound text (duden html -> anki format)
        
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
            # at the same time add link to dict __links
            self.__links[mp3_link.split('/')[-1]] = mp3_link
            span.string = '[sound:' + mp3_link.split('/')[-1] + ']'
            del span['title']
            del span['class']
        
        return unicode(soup)


'''
UnitTest
'''

def _UnitTest_AnkiRechtschreibung():
    
    # Rechtschreibung list for test
    lt = [u'Chip', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe']
    
    for item in lt:
        ars = AnkiRechtschreibung(item)
        
        print item, ':', ars.getWortText()
        print ars._handleSoundText(ars.sliceAussprache())
        print ars.getLinks()
        print ars.getTupleExampleAndDefinition()

if __name__ == '__main__':
    
    _UnitTest_AnkiRechtschreibung()