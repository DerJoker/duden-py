#!/usr/bin/python

import sys
import urllib
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

duden_main = 'http://www.duden.de'

r_search = 'rechtschreibung'

# 1st command line argument as word to search
to_search = sys.argv[1]

r_search_url = duden_main + '/' + r_search + '/' + to_search

duden_url = r_search_url
# print duden_url

f_result = urllib.urlopen(duden_url).read()
soup = BeautifulSoup(f_result)

t_result = soup.find_all("span", "helpref woerterbuch_hilfe_bedeutungen")
# print t_result

if len(t_result) > 0:
	i_result = len(t_result) - 1
	# span (find_all) -> h2 (parent) -> ... (next sibling)
	html_result = t_result[i_result].find_parent().find_next_sibling()
	# print html_result
	plain_result = ''
	for string in html_result.stripped_strings:
		plain_result = plain_result + '<div>' + string + '</div>'
	print plain_result