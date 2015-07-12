# coding: UTF-8

import urllib2

def read(url, retries=3, timeout=10):
    count = 0
    r = ''
    while (count < retries and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=timeout).read()
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

'''
UnitTest
'''

if __name__ == '__main__':
    print read('http://www.duden.de/rechtschreibung/dauern_waehren_durchhalten')