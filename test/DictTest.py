# coding: UTF-8

import Dict

# remove break line
wordList = [line.strip().decode('UTF-8') for line in open('WordList.txt').readlines() if line.strip() != '']

# wordList = [unicode(word, 'utf-8') for word in wordList]

# remove repeat
wordList = list(set(wordList))

print wordList

print len(wordList)

def GodicTest():
    
    for word in wordList:
        godic = Dict.Godic(word)
        godic.lookup()
        try:
            for definition in godic.definitions:
                print definition['content']
        except:
            print ''

def DudenTest():
    
    for word in wordList:
        duden = Dict.Duden(word)
        duden.lookup()
        try:
            for definition in duden.definitions:
                print definition['content']
        except:
            print ''

def LocalTest():
    localDict = Dict.Local()
    for word in wordList:
        localDict.addEntry(word)
    localDict.save()
    
    localDict = Dict.Local()
    for word in wordList:
        if localDict.godic.has_key(word.encode('UTF-8')):
            print localDict.godic[word.encode('UTF-8')]
        else:
            print word, 'not in Local Godic!'
        
        if localDict.duden.has_key(word.encode('UTF-8')):
            print localDict.duden[word.encode('UTF-8')]
        else:
            print word, 'not in Local Duden!'
    localDict.save()

# GodicTest()

# DudenTest()

LocalTest()