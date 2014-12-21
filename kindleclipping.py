# copy 'My Clippings.txt' from Kindle
clippings_handle = open('My Clippings.txt')

n_line = 0

for line in clippings_handle:
	n_line = n_line + 1
	if n_line % 5 == 4:
		print line