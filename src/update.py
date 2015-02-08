# coding: UTF-8

from bs4 import BeautifulSoup

import Dict

soup = BeautifulSoup(open('anki.html'))

# get wordList from anki.html

wordList = []

for item in soup.find_all('div', class_ = 'back'):
    for content in item.contents:
        try:
            words = content.strip('\n').split('\n')
            if words != ['']:
                wordList += words
        except:
            print content

# wordList = list(set(wordList))

print wordList
print len(wordList), 'words to update/add.'

# look up each word (and save locally)

localDict = Dict.Local()
for word in wordList:
    localDict.addEntry(word)
localDict.save()