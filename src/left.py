#!/usr/bin/python

# search for empty words

# f_awd = open('deutsch.txt')
f_awd = open('anki_word_definition.txt')

f_a = open('anki.txt', 'w')

# pattern: <div name="word_list"><h1>empty word</h1></div>
for line in f_awd.readlines():
    if line.find('</h1></div>') > 0:
        f_a.write(line.split('\t')[0] + '\n\n\n')
        
f_a.close()
f_awd.close()