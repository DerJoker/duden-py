#!/usr/bin/python

# copy 'My Clippings.txt' from Kindle
f_mc = open('My Clippings.txt')

n_line = 0

for line in f_mc:
	n_line = n_line + 1
	if n_line % 5 == 4:
		print line
		
f_mc.close()