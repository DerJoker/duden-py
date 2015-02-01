#!/usr/bin/python

from bs4 import BeautifulSoup

import Dict

soup = BeautifulSoup(open('anki.html'))

wordList = []

# create word list from anki.html
for item in soup.find_all('div', class_ = 'back'):
    try:
        wordList += item.string.encode('utf-8').split('\n')
    except:
        print 'Error in anki.html!'

wordList = list(set(wordList))

print wordList
print len(wordList)

# look up each word (locally)

localDict = Dict.Local()
localDict.update(wordList)
localDict.save()