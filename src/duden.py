#!/usr/bin/python

import urllib
from bs4 import BeautifulSoup

CODEC = 'utf-8'

"""
Duden
"""

d_rechtschreibung = 'http://www.duden.de/rechtschreibung/'
d_dudenonline = 'http://www.duden.de/suchen/dudenonline/'

class Duden:
	def __init__(self, word):
		self.word = word.encode(CODEC)
		self.dict = {}
		self.search()
	
	"""
	dudenonline suchen
	{(rechtschreibung_1, link_1), (rechtschreibung_2, link_2), ...}
	"""
	def search(self):
		d_suchen = d_dudenonline + self.word
		f_result = urllib.urlopen(d_suchen).read()
		soup = BeautifulSoup(f_result)
		l_link = soup.find_all('h3', text = self.word)
		for link in l_link:
			key = link.a['href'].split('/')[-1]
			self.dict[key] = d_rechtschreibung + key
	
	# rechtschreibung suchen
	def r_search(self):
		self.search()
		for key in self.dict:
			soup = BeautifulSoup(urllib.urlopen(d_rechtschreibung + key).read())
			t_result = soup.find_all('span', 'helpref woerterbuch_hilfe_bedeutungen')
			if len(t_result) > 0:
				# span (find_all) -> h2 (parent) -> ... (next sibling)
				html_result = t_result[-1].find_parent().find_next_sibling()
				self.dict[key] = html_result.prettify()
				# self.dict[key] = html_result.get_text()
	