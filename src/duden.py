#!/usr/bin/python

import sys
import urllib
from bs4 import BeautifulSoup

def duden_search(to_search):
	search_url = 'http://www.duden.de/suchen/dudenonline/' + to_search
	
	f_result = urllib.urlopen(search_url).read()
	soup = BeautifulSoup(f_result)
	
	definition_link_list = soup.find_all('h3', text = to_search)
	# print definition_link_list
	return definition_link_list

# write the definition to temp.txt (overwrite)
def write_temp(r_search_url):
	soup = BeautifulSoup(urllib.urlopen(r_search_url).read())
	t_result = soup.find_all("span", "helpref woerterbuch_hilfe_bedeutungen")
	if len(t_result) > 0:
		f_tmp = open('temp.txt', 'w')
		# span (find_all) -> h2 (parent) -> ... (next sibling)
		html_result = t_result[len(t_result) - 1].find_parent().find_next_sibling()
		f_tmp.write(html_result.prettify())
		f_tmp.close()

def get_definition():
	f_tmp = open('temp.txt')
	duden_def = '<div name="definition">'
	for line in f_tmp.readlines():
		duden_def = duden_def + line.strip()
	duden_def = duden_def + '</div>'
	f_tmp.close()
	return duden_def

reload(sys)
sys.setdefaultencoding('utf-8')

f_aw = open('anki_word.txt', 'r')
f_awd = open('anki_word_definition.txt', 'w')

n_line = 0

for line in f_aw.readlines():
	n_line = n_line + 1
	line = line.strip()
	if n_line % 3 == 1:
		s_sentence = line
		f_awd.write(s_sentence)
		f_awd.write('\t')
	elif n_line % 3 == 2:
		to_search_list = line.split(';')
		print to_search_list
		for to_search in to_search_list:
			to_search = to_search.strip()
			print to_search
			definition_link_list = duden_search(to_search)			
			for item in definition_link_list:
				r_search_url = 'http://www.duden.de/' + item.a['href']
				print r_search_url
				write_temp(r_search_url)
				f_awd.write(get_definition())
	else:
		f_awd.write('\n')

f_aw.close()
f_awd.close()