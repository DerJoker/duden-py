# coding: UTF-8

from bs4 import BeautifulSoup

soup = BeautifulSoup(open('edit.html').read().decode('utf-8'))

for item in soup.find_all('div', class_='note'):
    notes = item.string.split('\n')
    item.string = ''
    s = ''
    notes = ['<li>' + note + '</li>' for note in notes if note != '']
    for note in notes:
        s = s + note
    s = s + '<br />'
    item.append(BeautifulSoup(s))

f_tmp = open('anki.txt', 'w')
f_tmp.write(str(soup.body).replace('\n', '')
            .replace('<body>', '')
            .replace('</body>', '')
            .replace('><div class="front">', '>\n<div class="front">')
            .replace('<div class="back">', '\t<div class="back">')
#             .replace('<div class="reflink">', '<br /><div class="reflink">')
            )
f_tmp.close()