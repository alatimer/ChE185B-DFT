#!/usr/bin/env python

from ase.io import read,write
from ase.visualize import view
import sys
import numpy as np

def estimate_magmom(atoms,f=None):
    """
    Estimate magmom from log file (based on charge spheres centered on atoms) and assign to 
    atoms object to assist with calculation restart upon unexpected interruption
    """
    if not f:
        f = open('calcdir/log')
    else:
        f = open(f)
    lines = f.readlines()
    f.close()

    i = len(lines) - 1
    while True:
        if i == 0: raise IOError("Could not identify espresso magmoms")
        line = lines[i].split()
        if len(line) > 3:
            if line[0] == "absolute":
                abs_magmom = float(line[3])
        if len(line) > 6:
            if line[4] == "magn:":
                i -= len(atoms) - 1
                break
        i -= 1
    
    if abs_magmom < 1e-3:
        for atom in atoms:
            atom.magmom = 0
    else:
        total_esp_magmom = 0
        for j in range(len(atoms)):
            total_esp_magmom += np.abs(float(lines[i+j].split()[5]))

        for j in range(len(atoms)):
            atoms[j].magmom = round(float(lines[i+j].split()[5])*abs_magmom/total_esp_magmom,2)

if __name__ == '__main__':
    atoms = read(sys.argv[1])
    if len(sys.argv) > 2:
        f = sys.argv[2]
        estimate_magmom(atoms,f=f)
    else:
        estimate_magmom(atoms)
    view(atoms)

