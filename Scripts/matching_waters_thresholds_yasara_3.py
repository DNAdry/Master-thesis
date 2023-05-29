# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:07:51 2023

@author: adrian garcia herrero
"""

import os
import glob
import pandas as pd
import yasara

#Set desired threshold
threshold_1=1.00
threshold_2=1.2
threshold_3=1.4
threshold_4=1.6
threshold_5=1.8
threshold_6=2


#retreave directory names 
dirs = glob.glob("*/")
output = []

#Read Summary file
summary=[]
with open('Summary.tsv') as summary_file:
    for line in summary_file:
        summary.append(line.split('\t'))


#move to each one of the directories
for directory in dirs:
    if directory == '__pycache__\\':
        continue
    else:
        pdb_name=directory[0:4]
        os.chdir(pdb_name)
        current_dir=os.getcwd()
        crystal_compare_dir=current_dir[:-6]
        crystal_compare_dir+="1_Yasara\\%s"%pdb_name

# =============================================================================
# pdb_name="2vxt"
# os.chdir(pdb_name)
# current_dir=os.getcwd()
# =============================================================================


        #Start Yasara and set to blank
        yasara.run('DelObj all')
        #Load the pdb
        
        Load_crystal='LoadPDB "'+crystal_compare_dir+'\\Crystal_'+pdb_name+'.pdb\",Center=Yes,Correct=Yes'
        Load_predicted='LoadPDB "'+current_dir+'\\'+pdb_name+'_no-waters_Repair.pdb\",Center=Yes,Correct=Yes'
        yasara.run(Load_crystal)
        yasara.run(Load_predicted)
        print('Loaded - '+pdb_name)
        
        #Stablish number of Molecules in each object
        objects=yasara.run('ListObj Atom all')
        molecules=[]
        for obj in objects:
            yasara_out=yasara.run('ListMol Object '+ str(obj)+',MOLNAME')
            for i in range(0, len(yasara_out)):
                if yasara_out[i] == ' ':
                    yasara_out.pop(i)
                    break
            molecules.append(yasara_out)
        
        #Superimpose both Objects (PDB strcutures)
        superimpose='SupMol %s and Obj 1, Mol %s and Obj 2, Match=Yes, Flip=No, Unit=Obj' %(molecules[0][0],molecules[1][0])
        yasara.run(superimpose)
        
        #Obtain residues of each molecule
        residues=[[],[]]
        for i in range(0,2):
            for molecule in molecules[i]:
                if molecule == " ":
                    continue
                else:
                    res_list=yasara.run('ListRes Mol %s and Obj %s, RESNAME RESNUM' %(molecule, str(i+1)))
                    residues[i].append(res_list)
        
        
        #Delete non interface waters based on the number of molecules and interfaces of the pdb structure
        for pdb in summary:
            if pdb_name == pdb[0]:
                if pdb[2] != "NA":
                    yasara.run('DelRes HOH with distance > 8 from Mol %s %s' %(pdb[1],pdb[2]))    
                else:
                    Ab_mol=[pdb[1]]
                    yasara.run('DelRes HOH with distance > 8 from Mol %s' %pdb[1])
                    
                if "|" in pdb[4]:
                    ligand_mol=[pdb[4][0],pdb[4][-1]]
                    yasara.run('DelRes HOH with distance > 8 from Mol %s %s' %(pdb[4][0],pdb[4][-1]))
                    
                else:
                    yasara.run('DelRes HOH with distance > 8 from Mol %s' %(pdb[4]))
            
        
        #Change name of Mol containin the waters in both Objects so we can join them delete the protein structures of one of them and join them in one sigle Object with both waters in different Mol
        #Change water Mol names
        yasara.run('NameMol %s and Obj 1, W_C' %molecules[0][-1])
        yasara.run('NameMol %s and Obj 2, W_P' %molecules[1][-1])
        
        #Remove all but waters from object 2
        for del_mol in molecules[1]:
            yasara.run('DelMol %s and Obj 2' %del_mol)
            
        #Join Object 1 and 2 (Crystal and Predict) in Object 1
        yasara.run('JoinObj 1 2, 1')
        
        #Some color for visualizing
        yasara.run('ColorObj 1, Gray')
        yasara.run('ColorMol W_C, Blue')
        yasara.run('ColorMol W_P, Green')
        
        #Get number of waters in the interface from Crsystal and from Prediction
        crys_waters=len(yasara.run('ListRes Mol W_C, RESNAME RESNUM'))
        pred_waters=len(yasara.run('ListRes Mol W_P, RESNAME RESNUM'))
        
        
        #Obtain a list of every crystal water, their respective closest predicted water and the distance between them (to after filter with a threshold)
        #Obtain Crystal-Predict water pairs
        water_pairs=[]
        for res in residues[0][-1]:
            pred_w_pair = yasara.run('ListRes HOH Mol W_P with minimum distance from %s Mol W_C, RESNAME RESNUM' %res)
            if pred_w_pair != []:
                water_pairs.append([res, pred_w_pair[0]])
                
        #Get distances
        for i in range(0,len(water_pairs)):
            atom_C = yasara.run('ListRes %s Mol W_C, ATOMNUM' %water_pairs[i][0])[0]
            atom_P = yasara.run('ListRes %s Mol W_P, ATOMNUM' %water_pairs[i][1])[0]
            distance = yasara.run('Distance %s,%s' %(atom_C,atom_P))[0]
            water_pairs[i].append(distance)
        
        
        
        #Get the ratio of waters correctly predicted based on the stablished threshold
        num_crys_waters= len(water_pairs)
        num_matched_waters_1=0
        num_matched_waters_2=0
        num_matched_waters_3=0
        num_matched_waters_4=0
        num_matched_waters_5=0
        num_matched_waters_6=0
        distance_waters_1=0
        distance_waters_2=0
        distance_waters_3=0
        distance_waters_4=0
        distance_waters_5=0
        distance_waters_6=0
        
        for pair in water_pairs:
            if pair[2] <= threshold_1:
                num_matched_waters_1+=1
                if distance_waters_1==0:
                    distance_waters_1+=pair[2]
                else:
                    distance_waters_1= (distance_waters_1 + pair[2])/2
                    
            if pair[2] <= threshold_2:
                num_matched_waters_2+=1
                if distance_waters_2==0:
                    distance_waters_2+=pair[2]
                else:
                    distance_waters_2= (distance_waters_2 + pair[2])/2
                    
            if pair[2] <= threshold_3:
                num_matched_waters_3+=1
                if distance_waters_3==0:
                    distance_waters_3+=pair[2]
                else:
                    distance_waters_3= (distance_waters_3 + pair[2])/2
                    
            if pair[2] <= threshold_4:
                num_matched_waters_4+=1
                if distance_waters_4==0:
                    distance_waters_4+=pair[2]
                else:
                    distance_waters_4= (distance_waters_4 + pair[2])/2
                    
            if pair[2] <= threshold_5:
                num_matched_waters_5+=1
                if distance_waters_5==0:
                    distance_waters_5+=pair[2]
                else:
                    distance_waters_5= (distance_waters_5 + pair[2])/2
                    
            if pair[2] <= threshold_6:
                num_matched_waters_6+=1
                if distance_waters_6==0:
                    distance_waters_6+=pair[2]
                else:
                    distance_waters_6= (distance_waters_6 + pair[2])/2
                    
                
        ratio_waters_predicted_1=(num_matched_waters_1*100)/num_crys_waters
        ratio_waters_predicted_2=(num_matched_waters_2*100)/num_crys_waters
        ratio_waters_predicted_3=(num_matched_waters_3*100)/num_crys_waters
        ratio_waters_predicted_4=(num_matched_waters_4*100)/num_crys_waters
        ratio_waters_predicted_5=(num_matched_waters_5*100)/num_crys_waters
        ratio_waters_predicted_6=(num_matched_waters_6*100)/num_crys_waters
        
        out=[pdb_name+'.pdb', crys_waters, pred_waters, ratio_waters_predicted_1,ratio_waters_predicted_2,ratio_waters_predicted_3,ratio_waters_predicted_4,ratio_waters_predicted_5,ratio_waters_predicted_6,distance_waters_1,distance_waters_2,distance_waters_3,distance_waters_4,distance_waters_5,distance_waters_6]
        output.append(out) 
        
        #print('%.2f %% of waters correctly predicted with%2.f amstrong distance threshold' %(ratio_waters_predicted_1,threshold_1))
        #print('%.2f %% of waters correctly predicted with%2.f amstrong distance threshold' %(ratio_waters_predicted_2,threshold_2))
        #print('%.2f %% of waters correctly predicted with%2.f amstrong distance threshold' %(ratio_waters_predicted_3,threshold_3))
        #print('%.2f %% of waters correctly predicted with%2.f amstrong distance threshold' %(ratio_waters_predicted_4,threshold_4))
        #print('%.2f %% of waters correctly predicted with%2.f amstrong distance threshold' %(ratio_waters_predicted_5,threshold_5))
        #print('%.2f %% of waters correctly predicted with%2.f amstrong distance threshold' %(ratio_waters_predicted_6,threshold_6))
           
        
        #Save visualization of interface selection state
        yasara.run('SaveSce %s\\%s_Yasara_interface.sce' %(current_dir,pdb_name))
        
        os.chdir('..')


#transform output into a data frame
outdf= pd.DataFrame(output)
outdf.columns=["pdb","Num Crystal Waters in Interface","Num Predicted Waters in Interface","Ratio 1-Ams","Ratio 1.2-Ams","Ratio 1.4-Ams","Ratio 1.6-Ams","Ratio 1.8-Ams","Ratio 2-Ams","Distance 1-Ams","Distance 1.2-Ams","Distance 1.4-Ams","Distance 1.6-Ams","Distance 1.8-Ams","Distance 2-Ams"]
#output the commands in a excel file for easy acces
writer = pd.ExcelWriter("water_interface_results_yasara.xlsx", engine='xlsxwriter')
outdf.to_excel(writer, index=False)
writer.save() 
writer.close()
