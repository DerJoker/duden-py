# coding: UTF-8

from bs4 import BeautifulSoup

from duden import Rechtschreibung

class AnkiRechtschreibung(Rechtschreibung):
    
    def getLinks(self):
        return self.links
    
    def getCardExample(self):
        '''
        return list of (example/front, definition/back)
        '''
        aussprache = self.sliceAussprache()
        
        # add aussprache to back, and transform to anki sound text
        return [(beispiel, self.getWortText() + ' : ' + self._handleSoundText(self._handleImageText(bedeutung) + '<br >' + aussprache))
                for (beispiel, bedeutung) in self.getTupleExampleAndDefinition()]
    
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
            # at the same time add link to dict links
            self.links[mp3_link.split('/')[-1]] = mp3_link
            span.string = '[sound:' + mp3_link.split('/')[-1] + ']'
            del span['title']
            del span['class']
        
        return unicode(soup)
    
    def _handleImageText(self, text):
        '''
        handle sound text (duden html -> anki format)
        
        e.g.
        <span class="term_img">
            ...
            medium
            <img meta-type="image" meta-size="medium" meta-ref-id="201100282014" 
            meta-dateiname="Taetigkeit-201100282014.jpg" 
            meta-bu="Tätigkeit als Lehrer - ©&nbsp;MEV Verlag, Augsburg" 
            meta-alt="Tätigkeit - Tätigkeit als Lehrer" 
            meta-title="Tätigkeit - Tätigkeit als Lehrer" 
            src="http://duden.de/_media_/small/T/Taetigkeit-201100282014.jpg">
            
            full
            
            ...
        </span>
        ->
        <br ><span class="term_img"><img src="Taetigkeit-201100282014.jpg">
        <div>T\xe4tigkeit als Lehrer - \xa9\xa0MEV Verlag, Augsburg</div></img></span>
        '''
        soup = BeautifulSoup(text)
        
        for span_img in soup.find_all('span', class_='term_img'):
            img = span_img.find('img')
            src = img['src']
            src_local = src.split('/')[-1]
            self.links[src_local] = src
            meta = img['meta-bu']
            span_img.string = ''
            span_img.append(BeautifulSoup('<img src="' + src_local + '"><div>' + meta + '</div>'))
            
            # change span to div (new line)
            span_img.name = 'div'
            
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
        print ars.getCardExample()
        print ars.getLinks()

if __name__ == '__main__':
    
    _UnitTest_AnkiRechtschreibung()