# coding: UTF-8

from bs4 import BeautifulSoup

import Dict

d_anki = ''

class Slice:
    
    def __init__(self, word, definition, extra):
        self.word = str(word.encode('UTF-8'))
        self.definition = str(definition)
        self.extra = str(extra)
    
    def createAnki(self):
        s = '{{c1::' + self.word + '}} : ' + self.definition
        s += '\t'
        s += self.extra
        s += '\n'
        return s

def createSlices(word, strcontent):
    t_slices = []
    slices = []
    soup = BeautifulSoup(strcontent)
    for content in soup.contents[0].contents:
        if content.name == 'li':
            for subcontent in content.contents:
                if subcontent.name == 'ol':
                    for ssubcontent in subcontent.contents:
                        t_slices.extend(ssubcontent.contents)
                else:
                    t_slices.append(subcontent)
        if content.name == 'dd':
            t_slices.append(content)
    for content in t_slices:
        s = ''
        for div in content.find_all('div', recursive=False):
            s += str(div)
            content.div.decompose()
        slices.append(Slice(word, content,s))
    return slices

localDict = Dict.Local()

try:
    wdlist1 = eval(open('archive.txt').readline())
except:
    wdlist1 = []

print wdlist1

wdlist2 = []
soup = BeautifulSoup(open('anki.html'))

for item in soup.find_all('div', class_ = 'back'):
    for content in item.contents:
        try:
            words = content.strip().split('\n')
        except:
            words = ['']
        if words != ['']:
            wdlist2 += words

for word in list(set(wdlist2).difference(set(wdlist1))):
    print word
    # lookup in local duden
    if localDict.duden.has_key(word.encode('UTF-8')):
        res = localDict.duden[word.encode('UTF-8')]
        for definition in res:
            for sli in createSlices(word, definition['content']):
                d_anki += sli.createAnki()
    else: print 'Not found in local Dict Duden:', word

localDict.save()

f_danki = open('danki.txt', 'w')
f_danki.write(d_anki)
f_danki.close()