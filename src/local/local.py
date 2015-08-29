'''
Created on Aug 27, 2015

@author: feng
'''

import urllib2
import os.path

def read(url, retries=3, timeout=10):
    count = 0
    r = ''
    while (count < retries and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=timeout).read()
        except: pass
        count += 1
    return r

# download (read & save)
def download(url,local):
    r = read(url)
    if r != '':
        with open(local,'w') as f:
            f.write(r)
        return True
    else: return False

# folder name
FDN_RECHTSCHREIBUNG = 'rechtschreibung'
FDN_MEDIA = 'media'

if not os.path.exists(FDN_RECHTSCHREIBUNG):
    os.mkdir(FDN_RECHTSCHREIBUNG)

if not os.path.exists(FDN_MEDIA):
    os.mkdir(FDN_MEDIA)

def save_rechtschreibung(link, html_name):
    '''
    Return False if failed to download
    '''
    local = os.path.join(FDN_RECHTSCHREIBUNG, html_name)
    if not os.path.exists(local):
        return download(link, local)
    return True

def save_media(link, media_name):
    '''
    Return False if failed to download
    '''
    local = os.path.join(FDN_MEDIA, media_name)
    if not os.path.exists(local):
        return download(link, local)
    return True

def read_from_local(html_name):
    '''
    Return empty string '' if not exists
    '''
    local = os.path.join(FDN_RECHTSCHREIBUNG, html_name)
    if os.path.exists(local):
        return open(local).read()
    return ''

if __name__ == '__main__':
    # getrauen
    wort_rs = 'getrauen'
    link = 'http://www.duden.de/rechtschreibung/getrauen'
    print save_rechtschreibung(link, wort_rs + '.html')
    print read_from_local('getrauen.html')
    print read_from_local('no_result.html')