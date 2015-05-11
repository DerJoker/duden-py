# coding: UTF-8

import urllib
import urllib2
import os.path
from bs4 import BeautifulSoup

import config
import tools
from anki import CardImg
from anki import CardIdiom
from anki import CardExample

# sound download path
_path_duden_mp3 = config._path_duden_mp3
# picture download path
_path_duden_img = config._path_duden_img
# rechtschreibung html path
_path_rechtschreibung = config._path_rechtschreibung

'''
Class
'''

class Duden:
    
    def __init__(self):
        print 'Duden'

class Rechtschreibung:
    
    URLRECHTSCHREIBUNG = 'http://www.duden.de/rechtschreibung/'
    
    # access key
    k_img = 'img'
    k_text = 'text'
    k_def = 'definition'
    k_examples = 'examples'
    
    def __init__(self, d_rechtschreibung):
        self.rechtschreibung = d_rechtschreibung
        self.url = Rechtschreibung.URLRECHTSCHREIBUNG + d_rechtschreibung
        
        localRS = os.path.join(_path_rechtschreibung, self.rechtschreibung + '.html')
        if os.path.exists(localRS):
            self.html = open(localRS).read()
        else:
            self.html = tools.read(self.url).replace('\n', '')    # no newline, prepare for Anki card
            if self.html != '':
                with open(localRS,'w') as f:
                    f.write(self.html)
        
        self.soup = BeautifulSoup(self.html)
        
        try:
            # get_text() return Unicode
            self.wort = self.soup.find('span', class_='lemma_zeile').get_text().strip()
        except Exception,e:
            print d_rechtschreibung, e
            self.wort = ''
        
        # even if there's actually no mp3 for this word (in case we can find one someday ^_^)
        self.aussprache = self.rechtschreibung + '.mp3'
        
        self.bild = []
        
        self.beispiele = []
    
    def isValid(self):
        return self.rechtschreibung != '' and self.wort != ''
    
    '''
    -> str / unicode
    
    Return slice Aussprache.
    '''
    def sliceAussprache(self):
        return unicode(self.soup.find('div', class_='field-name-field-pronunciation'))
    
    '''
    -> [str]
    
    Return list of Bedeutungen / definitions with examples, if there is.
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
#         return [unicode(item) for item in l]
    
    # href="/rechtschreibung/weit" -> href="http://www.duden.de/rechtschreibung/weit"
    def completeRechtschreibungLinks(self):
        self.html = self.html.replace('href="/rechtschreibung/', 'href="' + Rechtschreibung.URLRECHTSCHREIBUNG)
    
    def downloadMP3(self):
        try:
            # it could happen that, there's no mp3 (e.g. sicher_machen)
            url_mp3 = self.soup.find('a', text="Als mp3 abspielen")['href']
            local_mp3 = os.path.join(_path_duden_mp3, self.aussprache)
            print 'start downloading pronunciation ...', self.wort
            urllib.urlretrieve(url_mp3, local_mp3)
            print url_mp3, 'downloaded.'
        except Exception,e:
            print e
    
    def downloadImg(self):
        imgs = self.soup.find_all('img', class_='hidden')
        
        for index in range(len(imgs)):
            text = str(imgs[index].find_next_sibling('span', class_='bu')).decode(tools.CODEC)
            
            url_img = imgs[index]['src']
            img_name = self.rechtschreibung + '-' + str(index) + '.' + url_img.split('.')[-1]
            local_img = os.path.join(_path_duden_img, img_name)
            print 'start downloading ...', img_name
            urllib.urlretrieve(url_img, local_img)
            print 'image downloaded.'
            
            content = BeautifulSoup(str(imgs[index].find_parent('span', class_='content')))
            for div in content.find_all(['div', 'span'],recursive=False):
                div.decompose()
            definition = str(content).decode(tools.CODEC)
                        
            self.bild.append({Rechtschreibung.k_img:img_name, Rechtschreibung.k_text:text, Rechtschreibung.k_def:definition})
    
    def getBeispiele(self):
        b = []
        
        beispiele = self.soup.find_all('div', class_='Beispiele')
        
        for beispiel in beispiele:
            bedeutung = BeautifulSoup(str(beispiel.parent))
            for div in bedeutung.find_all('div'):
                div.decompose()
            examples = []
            for bs in beispiel.find_all('span', class_='beispiel'):
                examples.append(str(bs).decode(tools.CODEC))
            b.append({Rechtschreibung.k_def:str(bedeutung).decode(tools.CODEC),Rechtschreibung.k_examples:examples})
        
        return b
    
    def makeCardExample(self):
        cards = []
        
        for item in self.getBeispiele():
            for example in item[Rechtschreibung.k_examples]:
                ce = CardExample(example,self.wort,item[Rechtschreibung.k_def],self.aussprache)
                if ce.isValid():
                    cards.append(ce.printCardExample())
                else: print 'Card Example invalid:', ce.printArgs()
        
        return cards
    
    def getWendungen(self):
        print 'Wendungen'
    
    def getBilder(self):
        bilder = []
        
        imgs = self.soup.find_all('img', class_='hidden')
        
        for img in imgs:
            text = str(img.find_next_sibling('span', class_='bu')).decode(tools.CODEC)
            
            # http://www.duden.de/_media_/full/S/Stellung-201100280769.jpg -> Stellung-201100280769.jpg
            img_name = img['src'].split('/')
            
            content = BeautifulSoup(str(img.find_parent('span', class_='content')))
            for div in content.find_all(['div', 'span'],recursive=False):
                div.decompose()
            definition = str(content).decode(tools.CODEC)
            
            bilder.append({Rechtschreibung.k_img:img_name, Rechtschreibung.k_text:text, Rechtschreibung.k_def:definition})
        
        return bilder

class Analyser:
    
    def __init__(self, html):
        self.html = html.replace('href="/rechtschreibung/', 'href="http://www.duden.de/rechtschreibung/')
    
    def getWord(self):
        soup = BeautifulSoup(self.html)
        if soup.find('span', class_='lemma_zeile') != None:
            return unicode(soup.find('span', class_='lemma_zeile')).strip()
        return ''
    
    def is_Wortschatz_des_Zertifikats_Deutsch(self):
        soup = BeautifulSoup(self.html)
        for div in soup.find_all('div',class_='field-name-field-didyouknow'):
            # example: nachdenken
            # Dieses Wort stand 1961 erstmals im Rechtschreibduden.
            # Dieses Wort gehört zum Wortschatz des Zertifikats Deutsch.
            contents = div.find_all('span',class_='content')
            for content in contents:
                if content.get_text().strip() == u'Dieses Wort gehört zum Wortschatz des Zertifikats Deutsch.':
                    return True
        return False
    
    def getLinkMP3(self):
        soup = BeautifulSoup(self.html)
        links = soup.find_all('a', text="Als mp3 abspielen")
        print len(links)
        if len(links) > 0:
            # it could happen that, there's no mp3 (e.g. sicher_machen)
            return soup.find('a', text="Als mp3 abspielen")['href']
        return None
    
    def getLinksIMG(self):
        soup = BeautifulSoup(self.html)
        return [img['src'] for img in soup.find_all('img', class_='hidden')]
    
    # return Recthschreibung on page without Blaettern part
    def getRechtschreibungOnPage(self):
        if self.html != '':
            soup = BeautifulSoup(self.html)
            # remove Blaettern part (Im Alphabet davor, Im Alphabet danach)
            soup.find('div', class_='field-name-field-browse').extract()
            # /rechtschreibung/fallen#b2-Bedeutung-1d -> fallen
            return [link['href'].split('/')[-1].split('#')[0] for link in soup.select('a[href^="http://www.duden.de/rechtschreibung/"]')]
        else: return []
    
    # return {definition1:[example1,example2...],definition2:[],...}
    def getExamples(self):
        examples = {}
        soup = BeautifulSoup(self.html)
        items = []
        items.extend(soup.find_all('div',class_='field-name-field-examples'))
        items.extend(soup.find_all('div',class_='field-name-field-abstract'))
        for item in items:
            for b in item.find_all('div',class_='Beispiele'):
                definition = unicode(b.parent)
                # remove divs like Beispiele and Wendungen, spans like term_img
                for c in b.parent.find_all(['div','span']):
                    definition = definition.replace(unicode(c),'')
                examples[definition] = [unicode(item) for item in b.find_all('span',class_='beispiel')]
        return examples

'''
UnitTest
'''

if __name__ == '__main__':
#     f_log = open('log.txt','w')
    
    # Rechtschreibung list for test
    lt = [u'Chip', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe', u'beobachten', u'modern_neu_modisch', u'schmuck', u'drauf', u'Anleitung']
#     lt = [u'verhe̲e̲rend']
    # WZD in wzd_list.txt
#     lt = [item.strip() for item in open('wzd_list.txt').readlines()]
    
    # special test cases of Sound
#     lt = [u'Aenderung', u'Aktivitaet', u'Anbieter', u'andere', u'Angestellter', u'ausreichend', u'Bedienungsanleitung', u'begeistert', u'Begruendung', u'Beratung', u'Bestaetigung', u'beste_Adjektiv', u'bestimmt_Adverb', u'Betreuung', u'Deutscher', u'Einfuehrung', u'Erhoehung', u'geboten_bieten', u'gestorben', u'Hersteller', u'interkulturell', u'Kindertagesstaette', u'langweilen', u'linke', u'Manager', u'maximal', u'naechste', u'Schlaf', u'Sekretaer', u'Traum_', u'vorige', u'aktiv', u'Alkohol', u'allerdings_Adverb', u'Artikel', u'Augenblick', u'augenblicklich', u'ausgezeichnet', u'benutzen', u'Cent', u'Chemie', u'dagegen', u'danach', u'darauf', u'darueber', u'deswegen', u'Dusche', u'Fleck', u'Geburt', u'gefallen_fallen', u'Geografie', u'gern', u'Hamburger_Speise_Gericht', u'Interesse', u'interessieren', u'Interview', u'Kilometer', u'Kredit_Finanzierung_Anleihe', u'Kritik', u'kritisch', u'Kurve', u'Langeweile', u'Motor', u'Motorrad', u'nachher', u'nutzen', u'passiv', u'Politik', u'Politiker', u'positiv', u'Scheck_Zahlungsanweisung_Bon', u'selbststaendig', u'Souvenir', u'Star_Kuenstler_Beruehmtheit', u'Stress', u'tatsaechlich_sicher_gewiss_garantiert', u'ueberall', u'unbedingt_zwingend', u'unheimlich', u'vorwaerts', u'Zentimeter', u'Arbeitnehmer', u'Balkon', u'Chance', u'dadurch', u'daher', u'darum', u'Mathematik', u'negativ', u'Saison', u'alltaeglich', u'Pension', u'Abteilung']
    
    for item in lt:
        rs = Rechtschreibung(item)
        
#         print rs.sliceAussprache()
        print item, ':', len(rs.sliceBedeutungen())
        print rs.sliceBedeutungen()
        
#         analyser = Analyser(rs.html)
#         analyser.getLinkMP3()
#         print analyser.getLinksIMG()
#         print analyser.getRechtschreibungOnPage()
#         print analyser.getExamples()
    
#     f_log.close()