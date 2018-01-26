#!/usr/bin/env python

import sys
path='/home/alatimer/che185b-drm/src/ase'
sys.path.insert(0,path)
from ase.lattice.surface import surface
from ase.io import read,write

lattice = read('init.traj')
indices = (1,1,1) ###change this to (2,1,1) and re-run...that should be it!
layers=4
vacuum=7.5

slab = surface(lattice,indices,layers,vacuum)

write('out.traj',slab)
