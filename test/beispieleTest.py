# coding: UTF-8

from beispiele import Rechtschreibung

t_rechtschreibung = 'sicher_machen'
# t_rechtschreibung = 'Rechtschreibfrage'
t_rechtschreibung = 'sicher_gefahrlos_tadellos_garantiert'

t_word = Rechtschreibung(t_rechtschreibung)

print t_word.wort

t_word.downloadMP3()

print t_word.getRechtschreibungOnPage()

print t_word.content
