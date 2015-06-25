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
        self.front = front.replace('\n','')
        self.back = back.replace('\n','')
        self.valid = True
    
    def isValid(self):
        return self.valid
    
    '''
    self -> str
    
    Make printable anki card string    
    '''
    def makeCard(self):
        s = '<div class="front">' + self.front + '</div>\t<div class="back">' + self.back + '</div>\n\n'
        return s.encode('utf-8')

class CardDefinition(Card):
    
    def __init__(self, word, definition, examples, sound):
        # front type Cloze
        self.front = u'{{c1::' + word + u'}} : ' + definition
        self.back = examples + u'<br>' + sound

class CardImg:
    
    def __init__(self, img, text, word, definition, pron):
        
        self.valid = True
        self.img = self.text = self.word = self.definition = self.pron = ''
        
        if isValidString(img) and isValidString(text):
            self.img = img.replace('\n','')
            self.text = text.replace('\n','')
            if isValidString(word) and isValidString(definition):
                self.word = word.replace('\n','')
                self.definition = definition.replace('\n','')
            if  isValidString(pron):
                self.pron = pron.replace('\n','')
        else:
            self.valid = False
    
    def isValid(self):
        return self.valid
    
    '''
    Q: img + text
    A: word : definition
       pron
    '''
    def printCardImg(self):
        s = ''
        if self.isValid():
            s_front = '<img src="' + self.img + '"><br>' + self.text
            s_back = ''
            if self.word != '' and self.definition != '':
                s_back += self.word + ' : ' + self.definition + '<br>'
            if self.pron != '':
                s_back += '[sound:' + self.pron + ']'
            s = '<div>' + s_front + '</div>\t<div>' + s_back + '</div>\n\n'
        return s

class CardIdiom:
    
    def __init__(self):
        print 'Card Idiom'
    
class CardExample(Card):
    
    def __init__(self, rechtschreibung, example, word, definition, sound):
        
        self.front = u'<div class="' + rechtschreibung + u'">' + example + u'</div>'
        self.back = word + u' : ' + definition + u'<br>' + sound
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
    pron = u'bekommen.mp3'
    
    # test Card
    cd = Card(front, back)
    print cd.makeCard()
    
    # test CardExample
    cdEx = CardExample(rs, example, word, definition, pron)
    cdEx.buildFrontStr()
    cdEx.buildBackStr()
    print cdEx.makeCard()