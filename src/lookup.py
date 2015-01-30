#!/usr/bin/python

import duden
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('anki.html'))

# look up each word

for item in soup.find_all('div', class_ = 'back'):
    if item != None:
        words = item.string.split()
        item.string = ''
        s = ''
        if len(words) == 0:
            s = '\n<pre>\n\n</pre>\n'
        else:
            for word in words:
                print word
                s = s + '\n<pre>\n' + word + '\n</pre>\n'
                d = duden.Duden(word)
                print d.dict
                for key in d.dict:
                    s = s + '<div><a href="' + d.dict[key][0] + '">' + key + '</a></div>\n'
                    s = s + '<div class="content">' + d.dict[key][1] + '</div>\n'
        item.append(BeautifulSoup(s))

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