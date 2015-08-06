# coding: UTF-8

import os.path

import sys
sys.path.append('..')
from tool import download

fdn_media = 'media'

if not os.path.exists(fdn_media):
    os.makedirs(fdn_media)

f_anki_links = open('links.txt')

for link in f_anki_links.readlines():
    link = link.strip()
    local = os.path.join(fdn_media, link.split('/')[-1])
    if not os.path.exists(local):
        download.download(link, local)

f_anki_links.close()