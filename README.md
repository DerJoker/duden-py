duden-py
========

### Info
Python 2.7.6

Beautiful Soup 4.3.2

### Description
Create importable Anki text (seperated by Tab) - Satz(Tab)Dedeutung von duden.de

kindleclipping.py - remove titles etc., keep only sentences, seperated by blank line

duden.py - scrape Bedeutungen und Beispiele from duden.de

### Steps:
- copy 'My Clippings.txt' from Kindle to the same folder as the script
- python kindleclipping.py > clippings.txt
- vim clippings.txt
- :r !python duden.py Aufnahme
- :%s/\n<div\>/\t<div\>/g
- import in Anki

### File list
- My Clippings.txt
- README.md
- duden.py
- kindleclipping.py