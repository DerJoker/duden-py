# coding: UTF-8

import os

'''
Configuration
'''

# folder name
_fn_mp3 = 'mp3'
_fn_img = 'img'
_fn_rs = 'rechtschreibung'

# path
_path_parent = os.path.abspath('..')
# sound download path
_path_duden_mp3 = os.path.join(_path_parent, _fn_mp3)
# picture download path
_path_duden_img = os.path.join(_path_parent, _fn_img)
# rechtschreibung html path
_path_rechtschreibung = os.path.join(_path_parent, _fn_rs)
