#!/usr/bin/python

import Dict

# remove break line
wordList = [line.strip() for line in open('WordList.txt').readlines() if line.strip() != '']

# remove repeat
wordList = list(set(wordList))

f = open('Satz.html', 'w')

f.write('<!DOCTYPE html>\n')
f.write('<html><head>' + 
        '<title>Satz</title>' + 
        '<meta http-equiv="Content-Type" content="text/py; charset=utf-8" />' + 
        '</head><body>\n')

for word in wordList:
    godic = Dict.Godic(word)
    godic.lookup()
    f.write(godic.definitions[0])

f.write('</body></html>')
f.close()