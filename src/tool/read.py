'''
Created on Jul 25, 2015

@author: feng
'''

import urllib2

def read(url, retries=3, timeout=10):
    count = 0
    r = ''
    while (count < retries and r == ''):
        try:
            r = urllib2.urlopen(url, timeout=timeout).read()
        except: pass
        count += 1
    return r