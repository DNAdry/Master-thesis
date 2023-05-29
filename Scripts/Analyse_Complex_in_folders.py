# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:50:40 2023

@author: adrian garcia herrero
"""
import os
import glob

#retreave directory names 
dirs = glob.glob("*/")

#create a job and config file for each one of the directories (one target pdb in each)
for directory in dirs:
    if directory == '__pycache__\\':
        continue
    else:
        pdb_name=directory[0:4]
        os.chdir(pdb_name)
        
        #Jobscript
        job=open("jobscript.sh", 'w')
        job.write("#!/bin/bash \n#$ -N AnalyseComplex \n#$ -V \n#$ -q all.q \n#$ -l h=!odin1&!odin2 \n#$ -l mem_limit=5G \n#$ -cwd \n./../foldx4 -f config_analyse_complex.cfg")
        job.close()
        
        #Config.cfg
        config=open("config_analyse_complex.cfg", 'w')
        config.write("command=AnalyseComplex \npdb=%s.pdb" %(pdb_name))
        config.close()
        
        #Create symbolic link to rotabase
        os.system('ln -s /switchlab/group/tools/FoldXSourceCode/2020_FoldX4/rotabase.txt rotabase.txt')
        
        
        #executte the created job !!
        
        os.system('qsub jobscript.sh')
        os.chdir('..')