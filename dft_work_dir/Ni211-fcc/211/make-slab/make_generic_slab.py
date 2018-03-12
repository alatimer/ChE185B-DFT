#!/usr/bin/env python

from ase.lattice.surface import fcc111,fcc211,hcp0001,hcp10m10,add_adsorbate
from ase import io

#Using a=lattice constant from lattice optimization
slab = fcc211('Ni', size=(3,3,4),a=3.55816650391)
slab.center(vacuum=16.0, axis=2)

io.write('out.traj',slab)
