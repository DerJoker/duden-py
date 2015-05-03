# coding: UTF-8

'''
make Anki card
'''

def isValidString(s):
    if (isinstance(s, unicode) or isinstance(s, str)) and s != '':
        return True
    else: return False

class Card:
    
    def __init__(self, rechtschreibung, front, back):
        self.rechtschreibung = rechtschreibung
        self.front = front.replace('\n','')
        self.back = back.replace('\n','')
    
    '''
    self -> str
    
    Make printable anki card string    
    '''
    def makeCard(self):
        return '<div class="' + self.rechtschreibung + '">' + self.front + '</div>\t<div>' + self.back + '</div>\n\n'

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
    
class CardExample:
    
    def __init__(self, example, word, definition, pron):
        
        self.backup = [example, word, definition, pron]
        
        self.valid = True
        self.example = self.word = self.definition = self.pron = ''
        
        if isValidString(example):
            self.example = example.replace('\n','')
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
    return string
    
    Q: example
    A: word : definition
       pron
    '''
    def printCardExample(self):
        s = ''
        if self.isValid():
            s_front = self.example
            s_back = ''
            if self.word != '' and self.definition != '':
                s_back += self.word + ' : ' + self.definition + '<br>'
            if self.pron != '':
                s_back += '<div>[sound:' + self.pron + ']</div>'
            s = '<div>' + s_front + '</div>\t<div>' + s_back + '</div>\n\n'
        return s.encode('utf-8')
    
    def printArgs(self):
        return type(self.backup[0]), self.backup[0]

'''
UnitTest
'''

if __name__ == '__main__':
    rs = u'bekommen'
    front = u'<span class="beispiel"><span class="font_normal">das Buch ist nicht mehr zu bekommen</span></span>'
    back = u'<span class="lemma_zeile"> <span class="lemma">be­kom­men</span> </span> : <span class="content">kaufen können, (gegen Geld) erhalten</span><br /><div>[sound:bekommen.mp3]</div>'
    cd = Card(rs, front, back)
    print cd.makeCard()