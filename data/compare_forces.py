import h5py
import numpy as np
import matplotlib.pyplot as plt

"""
example: compare the forces from the PBE dataset to the ones in the QMC dataset
WARNING: this will go through all of the forces in the QMC data,
    which may take some time for a small computer
"""

# the samples don't all have the same number of atoms,
# so the arrays in the data don't all have the same shape
# here we just flatten everything
forces_pbe = np.array([])
forces_qmc = np.array([])
f_pbe = h5py.File('pbe.hdf5', 'r')
f_qmc = h5py.File('qmc.hdf5', 'r')

index = f_pbe['selected_indices'][...]
for i in range(2000): # 2000 samples
    # index[i] in the PBE dataset is i in the QMC dataset
    forces_pbe = np.append(forces_pbe, f_pbe['forces/%d' % index[i]][...])
    # QMC data has an extra 3 columns for error bars
    forces_qmc = np.append(forces_qmc, f_qmc['forces/%d' % i][...][:,:3])

difference = forces_qmc - forces_pbe
print('RMS difference: %s' % (np.sqrt(np.mean(difference**2))))

# make a fitting scatterplot
plt.scatter(forces_qmc, forces_pbe)
plt.xlabel('RQMC force (eV/A)')
plt.ylabel('PBE force (eV/A)')
# plot x = y as a guide to the eye
x = [np.min(forces_qmc), np.max(forces_qmc)]
plt.plot(x, x)
plt.show()

# or more interestingly, plot the difference
plt.scatter(forces_qmc, forces_qmc - forces_pbe)
plt.xlabel('RQMC force (eV/A)')
plt.ylabel('RQMC force - PBE force (eV/A)')
plt.grid() # to guide the eye
plt.show()
