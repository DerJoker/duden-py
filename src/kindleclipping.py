#!/usr/bin/python

# copy 'My Clippings.txt' from Kindle
f_mc = open('My Clippings.txt')
f_a = open('anki.txt', 'w')

n_line = 0

for line in f_mc:
	n_line = n_line + 1
	if n_line % 5 == 4:
		f_a.write(line)
		f_a.write('\n')

print 'converted, see anki.txt'

f_a.close()		
f_mc.close()