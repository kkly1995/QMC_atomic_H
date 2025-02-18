import h5py
from ase import Atoms
from ase.io import write
from ase.calculators.singlepoint import SinglePointCalculator

"""
example: create an xyz file using all of the samples in qmc.h5
the data is already in ASE's native units
"""

samples = []
with h5py.File('qmc.h5', 'r') as f:
    for i in range(2000): # there are 2000 samples in this dataset
        r = f['positions/'  + str(i)][...]
        cell = f['cell/'    + str(i)][...]
        energy = f['energy/'+ str(i)][...][0] # second entry is the error bar
        forces = f['forces/'+ str(i)][...][:,:3] # last 3 columns are error bars
        # one could manually write everything in XYZ format,
        # but here we do it through ASE
        structure = Atoms('H' + str(len(r)),
                          positions = r,
                          cell = cell,
                          pbc = True,)
        calc = SinglePointCalculator(structure,
                                     energy = energy,
                                     forces = forces,)
        structure.calc = calc
        samples.append(structure)
write('qmc.xyz', samples)
