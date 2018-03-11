#!/usr/bin/python

#SBATCH -p normal
#SBATCH --output=lattice.out
#SBATCH --error=lattice.err
#SBATCH --time=20:00:00                                 #default is 20 hours
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END,FAIL                            #get emailed about job BEGIN, END, or FAIL
#SBATCH  --mail-user=sanand94@stanford.edu
#SBATCH --ntasks-per-node=16                            #task to run per node; each node has 16 cores


import sys
#path='/home/alatimer/che185b-drm/src/ase'
#sys.path.insert(0,path)
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
a0=2.5 ##starting guesses for lattice constant

x0=[a0]  ##pack up vaariables to optimize over to pass to solver (in this case there is only one)
iter = 0
logfile = open('lattice_opt.log','a')
logfile.write('Energy\ta\n')
logfile.close()
atoms_list = []


def get_energy(x):
    "Function to create an atoms object with lattice parameters specified by x and obtain its energy using calc."
    global iter
    iter +=1
    calc = espresso(pw=600, #while optimizing lattice, use high pw/dw and kpts. We will optimize these later.
        dw = 6000,
        kpts = (12,12,12),
        nbands = -12,
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

    atoms = build.bulk(Mtl,crystalstructure='fcc',a=x[0])  #make a fcc unit cell with new lattice vector
    for atom in atoms:
        atom.magmom=3
    atoms_list.append(atoms)

    atoms.set_calculator(calc)
    write('out.traj',atoms)
    a=x[0]

    energy = atoms.get_potential_energy()
    logfile = open('lattice_opt.log','a')
    logfile.write('%s\t%s\n' %(energy,a))
    logfile.close()
    
    return energy

x = fmin(get_energy,x0,ftol=1e-3) #this can be changed to minimize(...method = method...) in scipy > v0.1
print x

