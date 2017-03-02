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
from espresso import espresso
from ase.io import read,write
import numpy as np

kpts_list = np.arange(4,12,1)
logfile = open('kpts.log','w')
logfile.write('Energy\tKpt\n')

def get_energy(kpt):
    calc = espresso(pw=600, #while optimizing lattice, use high pw/dw and kpts. We will optimize these later.
        dw = 6000,
        kpts = (kpt,kpt,kpt),
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
    
    atoms = read('init.traj') #pass optimized unit cell
    for atom in atoms:
        atom.magmom=2

    atoms.set_calculator(calc)

    energy = atoms.get_potential_energy()
    logfile = open('kpts.log','a')
    logfile.write('%s\t%s\n' %(energy,kpt))
    logfile.close()
    
    return energy

for kpt in kpts_list:
    get_energy(kpt)
