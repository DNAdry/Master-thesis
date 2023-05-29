# -*- coding: utf-8 -*-
"""
Created on Tue May  2 20:59:17 2023

@author: adrian garcia herrero
"""

import os
import glob
import yasara

#read all pdb files names in the current directory
current_dir=os.getcwd()
pdb_files = []
for file in glob.glob("*.pdb"):
    pdb_files.append(file)

#Load the pdbs (one by one)
for pdb in pdb_files:
    #Start Yasara and set to blank
    yasara.run('DelObj all')
    #Load PDB
    Load_pdb='LoadPDB "'+current_dir+'\\'+pdb+'\",Center=Yes,Correct=Yes'
    yasara.run(Load_pdb)
    #Remove the pdb waters    
    yasara.run("DelRes HOH")
    #Save the new pdb without waters
    yasara.run("SavePDB 1, %s_no-waters.pdb" %pdb[0:4])
    