#!/usr/bin/python

import duden
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('anki.html'))

# look up each word

for item in soup.find_all('div', class_ = 'back'):
    words = item.string.split()
    item.string = ''
    s = ''
    for word in words:
        print word
        s = s + '<div>\n' + word + '\n</div>\n'
        d = duden.Duden(word)
        print d.dict
        for key in d.dict:
            s = s + '<div><a href="' + d.dict[key] + '">' + key + '</a></div>\n'
    item.append(BeautifulSoup(s))

f = open('anki2.html', 'w')
f.write(str(soup))
f.close()