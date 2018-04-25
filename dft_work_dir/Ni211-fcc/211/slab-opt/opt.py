#!/home/vossj/suncat/bin/python

#SBATCH -p normal,owners
#SBATCH --job-name=opt.py
#SBATCH --output=myjob.out
#SBATCH --error=myjob.err
#SBATCH --time=48:00:00									#default is 20 hours
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END,FAIL							#get emailed about job BEGIN, END, or FAIL
#SBATCH --mail-user=sanand94@stanford.edu
#SBATCH --ntasks-per-node=16 							#task to run per node; each node has 16 cores

from ase.constraints import *
from ase.utils.geometry import *
from ase.lattice.spacegroup import *
#from ase.structure import bulk
from math import *
from ase.lattice.surface import *
from ase import *
from ase.io import read,write
from ase.optimize import QuasiNewton
from espresso import espresso
#import espresso
from ase.dft.bee import BEEF_Ensemble
import cPickle as pickle
import os.path
import os

if os.path.exists('qn.traj')==True  and os.stat("qn.traj").st_size > 0:
    atoms =read('qn.traj')
else:
    atoms = read('init.traj')
    # If needed, turn bulk into surface:
    ##atoms = atoms.repeat([1,1,2])
    ##atoms.cell[2][2] += 15

for atom in atoms:
    atom.magmom = 3

######################### Calculator ##########################

calc = espresso(pw=600,					#plane-wave cutoff
                dw=6000,			 #density cutoff
                xc='RPBE',		#exchange-correlation functional
                kpts=(3,3,1),       #k-point sampling;
                nbands=-100,			  #20 extra bands besides the bands needed to hold
										#the valence electrons
                sigma=0.1,		#default value, fd smearing
					 spinpol=True,
					 psppath='/home/alatimer/bin/psp/esp_psp_w_gbrvRu/',
                convergence= {'energy':1e-5,
										'mixing':0.1,
										'nmix':10,
										'mix':4,
										'maxsteps':500,  #Change to 500 for spin polarized
										'diag':'david'	  #Can change to 'cg' for spin polarized
										 },	#convergence parameters
                output = {'removesave': True,
                    },
                dipole={'status':True}, #dipole correction to account for periodicity in z
                outdir='calcdir')	#output directory for Quantum Espresso files

####################   Constraints   ####################

highest_surf_index = 35
z_list = [atom.z for atom in atoms if atom.index <= highest_surf_index]
thresh = sum(z_list)/len(z_list)
mask = [atom.z<thresh for atom in atoms]

fixatoms = FixAtoms(mask=mask)
constraints = [fixatoms]
atoms.set_constraint(constraints)

write('pre.traj',atoms)				#Can check all constraints after calc begins to run in pre.traj


####################### Optimization ###################
atoms.set_calculator(calc)
qn = QuasiNewton(atoms, trajectory='qn.traj', logfile='qn.log')
qn.run(fmax=0.05)


