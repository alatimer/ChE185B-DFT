#!/home/vossj/suncat/bin/python
#above line selects special python interpreter needed to run espresso
#SBATCH -p normal
#################
#set a job name
#SBATCH --job-name=myjob
#################
#a file for job output, you can check job progress
#SBATCH --output=myjob.out
#################
# a file for errors from the job
#SBATCH --error=myjob.err
#################
#time you think you need; default is one hour
#in minutes in this case
#SBATCH --time=2:00:00
#################
#number of nodes you are requesting
#SBATCH --nodes=1
#################
#SBATCH --mem-per-cpu=4000
#################
#get emailed about job BEGIN, END, and FAIL
#SBATCH --mail-type=ALL
#################
#who to send email to; please change to your email
#SBATCH  --mail-user=sanand94@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################

import sys
path='/home/sanand94/che185b-drm/src/ase'
sys.path.insert(0,path)

from ase.optimize import QuasiNewton
from espresso import espresso
from espresso.vibespresso import vibespresso
import cPickle as pickle
from ase import Atoms

a=20.0
c=a/2.
d = 1.16 # initial guess for bond length, experimental value
atoms = Atoms('CO2',positions=( [ c, c, c],
                                [c - d , c, c],
                                [c + d , c, c]),
                   magmoms=[0.0, 0.0,0.0],
                   cell=(a, a, a))

calc = espresso(pw=600,	#plane-wave cutoff
                dw=6000,		#density cutoff
                xc='RPBE',		#exchange-correlation functional
                kpts=(1,1,1), #k-point sampling
                nbands=-10,	#10 extra bands besides the bands needed to hold
                					#the valence electrons
                sigma=0.1,
                convergence= {'energy':1e-5,
					               'mixing':0.1,
					               'nmix':10,
					               'mix':4,
					               'maxsteps':500,
					               'diag':'david'
					                },	#convergence parameters
                outdir='calcdir')	#output directory for Quantum Espresso files

atoms.set_calculator(calc)

dyn = QuasiNewton(atoms, logfile='qn.log', trajectory='qn.traj')
dyn.run(fmax=0.05)

energy = atoms.get_potential_energy()

calc.stop()
