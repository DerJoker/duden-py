#!/usr/bin/python

from bs4 import BeautifulSoup

soup = BeautifulSoup(open('test.html'))

print 'item.append() div class="content2"'
for item in soup.find_all('div', class_ = 'back'):
    item.append(BeautifulSoup('<div class="content2">something</div>'))

print 'try to find div class="content2"'
if soup.find_all('div', class_ = 'content2') == []:
    print 'can\'t find what\'s appended'
else: print 'find it'
