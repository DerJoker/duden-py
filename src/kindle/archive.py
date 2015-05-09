# coding: UTF-8

from bs4 import BeautifulSoup

try:
    wdlist1 = eval(open('archive.txt').readline())
except:
    wdlist1 = []

print wdlist1

wdlist2 = []
soup = BeautifulSoup(open('anki.html'))

for item in soup.find_all('div', class_ = 'back'):
    for content in item.contents:
        try:
            words = content.strip().split('\n')
        except:
            words = ['']
        if words != ['']:
            wdlist2 += words

print list(set(wdlist2).difference(set(wdlist1)))

f_archive = open('archive.txt', 'w')
f_archive.write(str(list(set(wdlist1).union(set(wdlist2)))))
f_archive.close()