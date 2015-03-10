# coding: UTF-8

from bs4 import BeautifulSoup

import Dict

localDict = Dict.Local()

soup = BeautifulSoup(open('anki.html'))

for item in soup.find_all('div', class_ = 'back'):
    s = ''
    s_ref = '<div class="reflink">'
    wordList = []
    for content in item.contents:
        try:
            words = content.strip().split('\n')
            if words != ['']:
                wordList += words
                for word in words:
                    print word
                    s = s + '\n<div class="note">\n' + word + '\n</div>\n<div class="definition-py">'
                    # lookup in local duden
                    if localDict.duden.has_key(word.encode('UTF-8')):
                        res = localDict.duden[word.encode('UTF-8')]
                        s = s + '<div class="duden">'
                        for definition in res:
                            s = s + definition['content']
                            s_ref = s_ref + '<div><a href="' + definition['url'] + '">' + definition['display'] + '</a></div>'
                        s = s + '</div>'
                    else: print 'Not found in local Dict Duden:', word
                    
                    # lookup in local godic
                    if localDict.godic.has_key(word.encode('UTF-8')):
                        res = localDict.godic[word.encode('UTF-8')]
                        s = s + '<div class="godic">'
                        for definition in res:
                            s = s + definition['content'].decode('utf-8')
                        s = s + '</div>'
                    else: print 'Not found in local Dict Godic:', word
                    
                    s = s + '</div>'
        except:
            s = s + '\n' + str(content).decode('UTF-8') + '\n'
    
    if len(wordList) == 0 and s == '':
        s = '\n<div class="note">\n\n</div>\n'
    
    s_ref = s_ref + '</div>'
    s = s + s_ref
    item.clear()
    item.append(BeautifulSoup(s))

localDict.save()

# view

f_view = open('view.html', 'w')
f_view.write(str(soup))
f_view.close()

# edit (delete definition-py)

soup = BeautifulSoup(open('view.html'))

for item in soup.find_all('div', class_ = 'definition-py'):
    item.decompose()

f_edit = open('edit.html', 'w')
f_edit.write(str(soup).replace('<div class="front">', '\n\n<div class="front">')
             .replace('</div>\n\n</div>','</div>\n</div>')
             )
f_edit.close()