'''
Created on Jul 25, 2015

@author: feng
'''

from read import read

# download (read & save)
def download(url,local):
    r = read(url)
    if r != '':
        with open(local,'w') as f:
            f.write(r)
        return True
    else: return False