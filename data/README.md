`pbe.h5` and `qmc.h5` contain our PBE and RQMC datasets in HDF5 format, respectively. The HDF5 structure is as follows:
```
$ h5ls qmc.h5
cell                     Group
energy                   Group
forces                   Group
positions                Group
```
```
$ h5ls qmc.h5/cell
0                        Dataset {3, 3}
1                        Dataset {3, 3}
10                       Dataset {3, 3}
100                      Dataset {3, 3}
1000                     Dataset {3, 3}
1001                     Dataset {3, 3}
...
```
where `0` is the 3 by 3 cell matrix for the 0th sample in the set. The other groups are similarly organized: for example, `qmc.h5/positions/0` is an N by 3 array giving the coordinates of the 0th sample. By combining these, one may reconstruct each configuration; see the example python scripts `to_xyz.py` and `compare_forces.py`. All numbers are given in ASE's native units, eV and angstroms.
