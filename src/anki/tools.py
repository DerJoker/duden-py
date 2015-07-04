# coding: UTF-8

import urllib2

CODEC = 'UTF-8'
TIMEOUT = 10
TRY = 3

def read(url):
    count = 0
    r = ''
    while (count < TRY and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=TIMEOUT).read()
        except Exception,e:
            print e
            r = ''
        count += 1
    return r

# download (read & save)
def download(url,local):
    r = read(url)
    if r != '':
        with open(local,'w') as f:
            f.write(r)
        print url, 'download successfully!'
    else: print url, 'download failed!'