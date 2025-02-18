import numpy as np
import h5py
from scipy.interpolate import interp1d
from mace.calculators import MACECalculator
from ase import Atoms

"""
example: use the QMC-MACE model to calculate the forces of a given structure
"""

def evaluate_pair_potential(structure, v, dv):
    # given an ASE Atoms object (structure),
    # use a tabulated potential (v) and its derivative (dv)
    # to calculate the energy and forces
    pairs = structure.get_all_distances(mic=True, vector=True)
    norm = np.linalg.norm(pairs, axis=-1)
    energy_table = v(norm)
    force_table = dv(norm)
    total_energy = 0.5*np.sum(energy_table)
    # forces are a little trickier
    norm[np.diag_indices_from(norm)] = 1 # avoid division by zero
    force_table /= norm
    force_table = force_table[:,:,np.newaxis]*pairs
    total_forces = np.sum(force_table, axis=0)
    return total_energy, total_forces

# the full model is actually the MACE model + a short-ranged pair potential
# here, read the pair potential
table = np.loadtxt('HH.table', skiprows=5)
v = interp1d(table[:,1], table[:,2], bounds_error=False, fill_value=0)
dv = interp1d(table[:,1], table[:,3], bounds_error=False, fill_value=0)

# pick a sample from the dataset, turn into an ASE Atoms object
# since MACECalculator is an ASE calculator object
i = 200
with h5py.File('../data/qmc.hdf5', 'r') as f:
    r = f['positions/' + str(i)][...]
    cell = f['cell/' + str(i)][...]
    # also grab the energy and forces for comparison later
    energy_qmc = f['energy/' + str(i)][...][0]
    forces_qmc = f['forces/' + str(i)][...][:,:3]
structure = Atoms('H' + str(len(r)), positions=r, cell=cell, pbc=True)

# load MACE calculator (CPU)
calc = MACECalculator(model_path='cpu_hydrogen.model',
                      device='cpu',
                      default_dtype='float32',)
## load MACE calculator (GPU)
#calc = MACECalculator(model_path='hydrogen.model',
#                      device='cuda',
#                      default_dtype='float32',)

# calculate energy and forces
energy_pp, forces_pp = evaluate_pair_potential(structure, v, dv)
structure.calc = calc
energy_mace = structure.get_potential_energy()
forces_mace = structure.get_forces()
energy_model = energy_mace + energy_pp
forces_model = forces_mace + forces_pp

print('energy (QMC): %s' % energy_qmc)
print('energy (QMC-MACE): %s' % energy_model)
