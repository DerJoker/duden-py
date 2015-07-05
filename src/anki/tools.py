# coding: UTF-8

import urllib2

def read(url, retries=3, timeouts=10):
    count = 0
    r = ''
    while (count < retries and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=timeouts).read()
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