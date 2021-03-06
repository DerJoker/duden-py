#!/usr/bin/python

"""
copy 'My Clippings.txt' from Kindle
transfer to 'anki.html', keeping only sentences
"""

f_mc = open('My Clippings.txt')
f_a = open('anki.html', 'w')

f_a.write('<!DOCTYPE html>\n')

"""
title: Anki
charset: utf-8
css: anki.css
"""
f_a.write('<html><head>' + 
		'<title>Anki</title>' + 
		'<meta http-equiv="Content-Type" content="text/py; charset=utf-8" />' + 
		'<link rel="stylesheet" type="text/css" href="anki.css" />' + 
		'<script src="https://code.jquery.com/jquery-1.10.2.js"></script>' + 
		'<script type="text/javascript" src="anki.js"></script>' + 
		'</head><body>\n')

n_line = 0

for line in f_mc:
	n_line = n_line + 1
	if n_line % 5 == 4:
		f_a.write('<div class="front">')
		f_a.write(line.strip())
		f_a.write('</div>\n')
		f_a.write('<div class="back">\n\n</div>\n\n')

f_a.write('</body></html>')

f_a.close()		
f_mc.close()

print 'converted, see anki.html'