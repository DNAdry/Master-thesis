# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:33:55 2023

@author: adrian garcia herrero
"""

import os
import glob

#retreave directory names 
dirs = glob.glob("*/")

#move to each one of the directories
for directory in dirs:
    if directory == '__pycache__\\':
        continue
    else:
        pdb_name=directory[0:4]
        os.chdir(pdb_name)
        
        #clear dir
        os.system('rm CrystalWaters.*112*')
        os.chdir('..')