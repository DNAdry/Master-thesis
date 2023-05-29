# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:38:35 2023

@author: adrian garcia herrero
"""
import os
import glob

#read all pdb files names in the current directory
pdb_files = []
for file in glob.glob("*.pdb"):
    pdb_files.append(file)
    
#stablish maximun number of jobbs/files
file_max=1+len(pdb_files)//30


#Create all the needed files
file_num=0
while len(pdb_files)>0:    
    file_num=file_num + 1
    job=open("jobscript%d.sh" %(file_num),"w")
    job.write("#!/bin/bash \n#$ -N RepairPDBs \n#$ -V \n#$ -q all.q \n#$ -l h=!odin1&!odin2 \n#$ -l mem_limit=5G \n#$ -cwd \n./foldx4 -f config_%d.cfg" %(file_num))
    job.close()
    
    ############################### TO BE MODIFIED #######################################
    config=open("config_%d.cfg" %(file_num),"w")
    config.write("command=RepairPDB \npdb-list=list_%d.txt \nwater=-PREDICT \npdbWaters=true" %(file_num))
    config.close()
    ######################################################################################
    
    pdbs=[]
    if len(pdb_files)>file_max:
        for i in range(3):
            pdbs.append(pdb_files.pop(0))
    else:
        while len(pdb_files)>0:
            pdbs.append(pdb_files.pop(0))
            
    pdb_list=open("list_%d.txt"%(file_num),"w")
    for pdb in pdbs:
        pdb_list.write("%s\n" %(pdb))
    pdb_list.close()

#Executte the created job !!
    os.system('qsub jobscript%d.sh' %(file_num))
    
    


