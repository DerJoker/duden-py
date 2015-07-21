# coding: UTF-8

import os.path

import tools

fdn_media = 'media'

if not os.path.exists(fdn_media):
    os.makedirs(fdn_media)

f_anki_links = open('links.txt')

for link in f_anki_links.readlines():
    link = link.strip()
    local = os.path.join(fdn_media, link.split('/')[-1])
    if not os.path.exists(local):
        tools.download(link, local)

f_anki_links.close()