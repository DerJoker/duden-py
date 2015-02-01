#!/usr/bin/python

from bs4 import BeautifulSoup

import Dict

localDict = Dict.Local()

soup = BeautifulSoup(open('anki.html'))

for item in soup.find_all('div', class_ = 'back'):
    try:
        words = item.string.split()
        item.string = ''
        s = ''
        if len(words) == 0:
            s = '\n<pre>\n\n</pre>\n'
        else:
            for word in words:
                print word
                s = s + '\n<pre>\n' + word + '\n</pre>\n'
                try:
                    res = localDict.duden[word]
                    print res
                    i = 0
                    while i < len(res[0]):
                        s = s + '<div><a href="' + res[1][i] + '">' + res[0][i] + '</a></div>\n'
                        s = s + '<div class="content">' + res[2][i] + '</div>\n'
                        i = i + 1
                except:
                    print 'Not found in local Dict:', word
        item.append(BeautifulSoup(s))
    except:
        print 'Error in anki.html!'

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
             .replace('</pre>', '</pre>\n')
             .replace('</div>\n\n</div>','</div>\n</div>'))
f_edit.close()