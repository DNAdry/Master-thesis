# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:23:37 2023

@author: adrian garcia herrero
"""

import os

#reads directory files
dir_files = os.listdir()

#for each pdb file found creates a folder and puts every pdb and repaired pdb in its folder
for file in dir_files:
    if file[-3:] == "pdb": 
        name=file[0:4]
        if os.path.exists("%s/"%name):
            os.replace("%s"%(file), "%s/%s"%(name,file))
        else:    
            os.mkdir(name)
            os.replace("%s"%(file), "%s/%s"%(name,file))

    



