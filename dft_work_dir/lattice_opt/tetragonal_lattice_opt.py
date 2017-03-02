#!/home/vossj/suncat/bin/python

#SBATCH -p iric
#SBATCH --output=myjob.out
#SBATCH --error=myjob.err
#SBATCH --time=48:00:00                                 #default is 20 hours
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END,FAIL                            #get emailed about job BEGIN, END, or FAIL
#SBATCH  --mail-user=allegralatimer@gmail.com
#SBATCH --ntasks-per-node=16                            #task to run per node; each node has 16 cores


import sys
path='/home/alatimer/che185b-drm/src/ase'
sys.path.insert(0,path)
from ase import build
#import structures
from scipy.optimize import *
from espresso import espresso
import os
from ase.lattice.spacegroup import crystal
import copy
from ase.io import read,write
import math

import sys

Mtl='Ni'
a0=4.80 ##starting guesses for lattice constants
c0=6.84

x0=[a0,c0]  ##pack up vaariables to optimize over to pass to solver
iter = 0
logfile = open('lattice_opt.log','a')
logfile.write('Energy\ta\tb\tc\n')
logfile.close()
atoms_list = []


def get_energy(x):
    "Function to create an atoms object with lattice parameters specified by x and obtain its energy using calc."
    global iter
    iter +=1
    calc = espresso(pw=600, #while optimizing lattice, use high pw/dw and kpts. We will optimize these later.
        dw = 6000,
        kpts = (12,12,12),
        nbands = -100,
        xc = 'RPBE',
        convergence = {'energy':1e-5,
                       'mixing':0.1,
							  'nmix':10,
							  'mix':4,
                       'maxsteps':200,
                       'diag':'david'},
        dipole = {'status':False},
        spinpol = True,
        outdir = 'calcdir',
        output = {'removesave': True,},
        )

    #atoms=read('init.traj')
    atoms = build.bulk(Mtl,crystalstructure='fcc')#,a=x[0],c=x[1])
    #a = x[0]; b= x[0]; c=x[1] 
    #a_vec=np.array([1,0,0])*a
    #b_vec=np.array([-math.sin(math.pi/6),math.cos(math.pi/6),0])*b
    #c_vec=np.array([0,0,1])*c

    #atoms.set_cell(cell=[a_vec,b_vec,c_vec],scale_atoms=True)
    atoms_list.append(atoms)
    atoms.set_calculator(calc)
    write('out.traj',atoms_list)

    energy = atoms.get_potential_energy()
    logfile = open('lattice_opt.log','a')
    logfile.write('%s\t%s\t%s\t%s\n' %(energy,a,b,c))
    logfile.close()
    
    return energy

x = fmin(get_energy,x0,ftol=1e-3) #this can be changed to minimize(...method = method...) in scipy > v0.1
print x

