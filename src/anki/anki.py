# coding: UTF-8

import card

from bs4 import BeautifulSoup
from duden import Rechtschreibung

# Rechtschreibung list for test
lt = [u'verheerend', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe', u'beobachten', \
      u'modern_neu_modisch', u'schmuck', u'drauf', u'Anleitung', u'Abteilung', u'Pension']

# WZD in wzd_list.txt
# lt = [item.strip() for item in open('wzd_list.txt').readlines()]

f_anki_links = open('links.txt', 'w')

'''
Card Definition
'''

# f_anki_def = open('anki_definition_zd.txt', 'w')
#  
# for item in lt:
#     print item
#     word = Rechtschreibung(item).getWortText()
#     df = DudenFactory(item)
#     sound = df.getSoundText()
#     for (definition, examples) in df.getCardDefinitionWithExamples():
#         cd = anki.CardDefinition(word, definition, examples, sound)
#         f_anki_def.write(cd.makeCard())
#    
# f_anki_def.close()

'''
Card Example
'''

f_anki_examples = open('anki_examples_zd.txt', 'w')
 
for item in lt:
    print item
    rs = Rechtschreibung(item)
    word = rs.getWortText()
    for link in rs.getSoundLinks():
        f_anki_links.write(link + u'\n')
    sound = rs.getAnkiSound()
    for (example, definition) in rs.getTupleExampleAndDefinition():
        def_misc = definition + u'<br >' + sound
        cd = card.CardExample(item, example, word, def_misc)
        f_anki_examples.write(cd.makeCard() + '\n')
  
f_anki_examples.close()

f_anki_examples2 = open('anki_examples_zd2.txt', 'w')
with open('anki_examples_zd.txt') as f:
    
    s = f.read()
    
    soup = BeautifulSoup(s)
    
    # Sound
    
    # div class="Aussprache"
    
    # span class="audio"
    for span in soup.findAll('span', class_='audio'):
        mp3_link = span.find('a', text='Als mp3 abspielen')['href']
        span.string = '[sound:' + mp3_link.split('/')[-1] + ']'
        del span['title']
        del span['class']
    
    # new line before image, and tab before card back side
    s = str(soup).replace('<span class="term_img">', '<br ><span class="term_img">').replace('<div class="back">', '\t<div class="back">')
    
f_anki_examples2.write(s)
f_anki_examples2.close()

f_anki_links.close()