# coding: UTF-8

import urllib2
import logging

def read(url, retries=3, timeout=10):
    count = 0
    r = ''
    while (count < retries and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=timeout).read()
        except Exception,e:
            logging.info(e)
            r = ''
        count += 1
    return r

# download (read & save)
def download(url,local):
    r = read(url)
    if r != '':
        with open(local,'w') as f:
            f.write(r)
        logging.info(url + ' download successfully!')
    else: logging.info(url + ' download failed!')

'''
UnitTest
'''

if __name__ == '__main__':
#     print read('http://www.duden.de/rechtschreibung/dauern_waehren_durchhalten')
    print read('http://www.duden.de/suchen/dudenonline/stän­dig')