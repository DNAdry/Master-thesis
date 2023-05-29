# Create cysteine bridges
import os,sys,glob,subprocess,time
import yasara

yasara.info.mode = 'txt'

startingDir = os.getcwd()

pdbs = sorted(glob.glob('./Candidates/*.pdb'),reverse=True)

surffile = open('Cavities.txt','w')
surffile.write('RepairPDB\tInterfaceSurfaceArea\tCavityVolumeTotal\tCavityVolumeLig\tCavityVolumeAb\tCavityVolumeInt\tChargeLig\tChargeAb\tPiPiEn\tPiPiNum\tPiPiDist\tCationPi\tIonic\tHydrophobic\n')
print(len(pdbs))

LigandMol = 'A'

for pdb in pdbs:
	name = pdb.split('/')[-1].split('.')[0]
	rawpdb = pdb.split('/')[-1]
	yasara.run('DelObj all')
	LoadCommand = 'LoadPDB \"'+startingDir+pdb.replace('./','/')+'\",Center=Yes,Correct=Yes'
	print(LoadCommand)
	yasara.run(LoadCommand)
	yasara.run('DelRes !Protein')
	try:
		yasara.run('CleanAll')
	except:
		continue
	yasara.run('ForceField YASARA2,SetPar=Yes')
	yasara.run('AddHydAll')
	#mols = yasara.run('ListMol all,Format=MOLNAME')
	#print(mols)
	surf1 = yasara.run('ConSurfMol '+LigandMol+' and Obj 1,Mol !'+LigandMol+' and Obj 1')
	#print(surf1)
	surf2 = yasara.run('ConSurfMol !'+LigandMol+' and Obj 1,Mol '+LigandMol+' and Obj 1')
	#print(surf2)
	surfmean = (float(surf1[0])+float(surf2[0]))/2
	cavityFull = yasara.run('CaviVolObj 1,Type=Molecular')
	cavityLig = yasara.run('CaviVolMol '+LigandMol+',Type=Molecular')
	cavityAb = yasara.run('CaviVolMol !'+LigandMol+',Type=Molecular')
	try:
		DistanceCentre = yasara.run('GroupDistance Mol '+LigandMol+',Mol !'+LigandMol+'')
	except:
		continue
	chargeLig = yasara.run('ChargeMol '+LigandMol+'')
	chargeAb = yasara.run('ChargeMol !'+LigandMol+'')
	pipiglobal = yasara.run('ListIntMol '+LigandMol+',!'+LigandMol+',Type=PiPi,Cutoff=5.0,Exclude=4,Occluded=Yes,Sort=No,Results=5')[4:][::5]
	pipiglobalnum = yasara.run('ListIntMol '+LigandMol+',!'+LigandMol+',Type=PiPi,Cutoff=5.0,Exclude=4,Occluded=Yes,Sort=No,Results=5')[3:][::5]
	pipiglobaldist = yasara.run('ListIntMol '+LigandMol+',!'+LigandMol+',Type=PiPi,Cutoff=5.0,Exclude=4,Occluded=Yes,Sort=No,Results=5')[2:][::5]
	cationpiglobal = yasara.run('ListIntMol '+LigandMol+',!'+LigandMol+',Type=CationPi,Cutoff=5.0,Exclude=4,Occluded=Yes,Sort=No,Results=5')[4:][::5]
	ionicglobal = yasara.run('ListIntMol '+LigandMol+',!'+LigandMol+',Type=Ionic,Cutoff=5.0,Exclude=4,Occluded=Yes,Sort=No,Results=5')[4:][::5]
	hydrophobicglobal = yasara.run('ListIntMol '+LigandMol+',!'+LigandMol+',Type=Hydrophobic,Cutoff=5.0,Exclude=4,Occluded=Yes,Sort=No,Results=5')[4:][::5]
	if len(hydrophobicglobal)==1:
		hydrophobicglobal = float(hydrophobicglobal[0])
	elif len(hydrophobicglobal)==0:
		hydrophobicglobal = 0
	else:
		hydrophobicsum = 0
		for hydrophobic in hydrophobicglobal:
			hydrophobicsum = hydrophobicsum + float(hydrophobic)
		hydrophobicglobal = hydrophobicsum
	if len(ionicglobal)==1:
		ionicglobal = float(ionicglobal[0])
	elif len(ionicglobal)==0:
		ionicglobal = 0
	else:
		ionicsum = 0
		for ionic in ionicglobal:
			ionicsum = ionicsum + ionic
		ionicglobal = ionicsum
	if len(cationpiglobal)==1:
		cationpiglobal = cationpiglobal[0]
	elif len(cationpiglobal)==0:
		cationpiglobal = 0
	else:
		cationpisum = 0
		for cationpi in cationpiglobal:
			cationpisum = cationpisum + cationpi
		cationpiglobal = cationpisum
	if len(pipiglobal)==1:
		pipiglobal = pipiglobal[0]
	elif len(pipiglobal)==0:
		pipiglobal = 0
	else:
		pipisum = 0
		for pipi in pipiglobal:
			pipisum = pipisum + pipi
		pipiglobal = pipisum
	if len(pipiglobalnum)==1:
		pipiglobalnum = pipiglobalnum[0]
	elif len(pipiglobalnum)==0:
		pipiglobalnum = 0
	else:
		pipisum = 0
		for pipi in pipiglobalnum:
			pipisum = pipisum + pipi
		pipiglobalnum = pipisum
	if len(pipiglobaldist)==1:
		pipiglobaldist = pipiglobaldist[0]
	elif len(pipiglobaldist)==0:
		pipiglobaldist = 0
	else:
		pipisum = 0
		for pipi in pipiglobaldist:
			pipisum = pipisum + pipi
		pipiglobaldist = pipisum
	if len(chargeAb)==1:
		chargeAb = chargeAb[0]
	elif len(chargeAb)==0:
		chargeAb = 0
	else:
		chargeAbsum = 0
		for chargeAb1 in chargeAb:
			chargeAbsum = chargeAbsum + chargeAb1
		chargeAb = chargeAbsum
	if len(chargeLig)==1:
		chargeLig = chargeLig[0]
	elif len(chargeLig)==0:
		chargeLig = 0
	else:
		chargeLigsum = 0
		for chargeLig1 in chargeLig:
			chargeLigsum = chargeLigsum + chargeLig1
		chargeLig = chargeLigsum
	cavityInt = float(cavityFull[0])-float(cavityLig[0])-float(cavityAb[0])
	surffile.write(pdb.split('/')[-1]
		+'\t'+str(surfmean)
		+'\t'+str(cavityFull[0])
		+'\t'+str(cavityLig[0])
		+'\t'+str(cavityAb[0])
		+'\t'+str(cavityInt)
		+'\t'+str(round(chargeLig))
		+'\t'+str(round(chargeAb))
		+'\t'+str(pipiglobal)
		+'\t'+str(pipiglobalnum)
		+'\t'+str(pipiglobaldist)
		+'\t'+str(cationpiglobal)
		+'\t'+str(ionicglobal)
		+'\t'+str(hydrophobicglobal)
		+'\n')
	surffile.flush()
	

surffile.close()
