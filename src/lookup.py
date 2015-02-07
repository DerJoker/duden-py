#!/usr/bin/python

from bs4 import BeautifulSoup

import Dict

soup = BeautifulSoup(open('anki.html'))

wordList = []

# create word list from anki.html
for item in soup.find_all('div', class_ = 'back'):
    try:
        wordList += item.string.split('\n')
    except:
        print 'Error in anki.html!'

wordList = list(set(wordList))

wordList = [word.strip() for word in wordList if word.strip() != '']

print wordList
print len(wordList)

# look up each word (and save locally)

localDict = Dict.Local()
for word in wordList:
    localDict.addEntry(word)
localDict.save()