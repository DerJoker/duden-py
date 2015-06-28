# coding: UTF-8

'''
make Anki card
'''

def isValidString(s):
    if (isinstance(s, unicode) or isinstance(s, str)) and s != '':
        return True
    else: return False

class Card:
    
    def __init__(self, front, back):
        self.front = front
        self.back = back
        self.valid = True
    
    def isValid(self):
        return self.valid
    
    '''
    self -> str
    
    Make printable anki card string, seperate by tab
    '''
    def makeCard(self):
        self.front = self.front.replace('\n','')
        self.back = self.back.replace('\n','')
        s = u'<div class="front">' + self.front + u'</div>\t<div class="back">' + self.back + u'</div>'
        return s.encode('utf-8')

class CardDefinition(Card):
    
    def __init__(self, word, definition, examples, sound):
        # front type Cloze
        self.front = u'{{c1::' + word + u'}} : ' + definition
        self.back = examples + u'<br>' + sound

class CardImg:
    
    def __init__(self):
        print 'Card Image'

class CardIdiom:
    
    def __init__(self):
        print 'Card Idiom'
    
class CardExample(Card):
    
    def __init__(self, rechtschreibung, example, word, def_misc):
        
        self.front = u'<div class="' + rechtschreibung + u'">' + example + u'</div>'
        self.back = word + u' : ' + def_misc
        self.valid = True

'''
UnitTest
'''

if __name__ == '__main__':
    
    front = u'<div class="bekommen"><span class="beispiel"><span class="font_normal">das Buch ist nicht mehr zu bekommen</span></span></div>'
    back = u'<span class="lemma_zeile"> <span class="lemma">be­kom­men</span> </span> : <span class="content">kaufen können, (gegen Geld) erhalten</span><br /><div>[sound:bekommen.mp3]</div>'
    
    rs = u'bekommen'
    example = u'<span class="beispiel"><span class="font_normal">das Buch ist nicht mehr zu bekommen</span></span>'
    word = u'<span class="lemma_zeile"> <span class="lemma">be­kom­men</span> </span>'
    definition = u'<span class="content">kaufen können, (gegen Geld) erhalten</span>'
    
    # test Card
    cd = Card(front, back)
    print cd.makeCard()
    
    # test CardExample
    cdEx = CardExample(rs, example, word, definition)
    print cdEx.makeCard()