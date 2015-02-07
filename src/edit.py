#!/usr/bin/python

from bs4 import BeautifulSoup

import Dict

def makeHyperlink(display, link):
    return '<div><a href="' + link + '">' + display + '</a></div>\n'

localDict = Dict.Local()

soup = BeautifulSoup(open('anki.html'))

for item in soup.find_all('div', class_ = 'back'):
#     try:
    words = item.string.split()
    item.string = ''
    s = ''
    if len(words) == 0:
        s = '\n<div class="note">\n\n</div>\n'
    else:
        s_ref = '<div class="reflink">'
        for word in words:
            print word
            s = s + '\n<div class="note">\n' + word + '\n</div>\n'
            # lookup in local duden
            if localDict.duden.has_key(word.encode('UTF-8')):
                res = localDict.duden[word.encode('UTF-8')]
                s = s + '<div class="duden" class="content">'
                for definition in res:
                    s = s + definition['content']
                    s_ref = s_ref + '<div><a href="' + definition['url'] + '">' + definition['display'] + '</a></div>'
                s = s + '</div>'
            else: print 'Not found in local Dict Duden:', word
            
            # lookup in local godic
            if localDict.godic.has_key(word.encode('UTF-8')):
                res = localDict.godic[word.encode('UTF-8')]
                s = s + '<div class="godic" class="content">'
                for definition in res:
                    s = s + definition['content'].decode('utf-8')
                s = s + '</div>'
            else: print 'Not found in local Dict Godic:', word

        s_ref = s_ref + '</div>'
        s = s + s_ref
    item.append(BeautifulSoup(s))
#     except:
#         print 'Error in anki.html!'

localDict.save()

# view

f_view = open('view.html', 'w')
f_view.write(str(soup))
f_view.close()

# edit (delete content)

soup = BeautifulSoup(open('view.html'))

for item in soup.find_all('div', class_ = 'content'):
    item.decompose()

f_edit = open('edit.html', 'w')
f_edit.write(str(soup).replace('<div class="front">', '\n\n<div class="front">')
             .replace('</div>\n\n</div>','</div>\n</div>'))
f_edit.close()