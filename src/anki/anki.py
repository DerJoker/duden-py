# coding: UTF-8

import card

from bs4 import BeautifulSoup
from duden import Rechtschreibung

# Rechtschreibung list for test
lt = [u'verheerend', u'Taetigkeit', u'Blickwinkel', u'scheiden', u'Ehe', u'beobachten', \
      u'modern_neu_modisch', u'schmuck', u'drauf', u'Anleitung']

# WZD in wzd_list.txt
# lt = [item.strip() for item in open('wzd_list.txt').readlines()]

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
    sound = rs.sliceAussprache()
    for (example, definition) in rs.getTupleExampleAndDefinition():
        def_misc = definition + u'<br >' + sound
        cd = card.CardExample(item, example, word, def_misc)
        f_anki_examples.write(cd.makeCard() + '\n')
 
f_anki_examples.close()

