#!/usr/bin/env python

from ase.lattice.surface import fcc111,fcc211,hcp0001,hcp10m10,add_adsorbate
from ase import io

#Using a=lattice constant from lattice optimization
slab = fcc211('Co', size=(3,3,4),a=2.5071)
slab.center(vacuum=16.0, axis=2)

io.write('out.traj',slab)
