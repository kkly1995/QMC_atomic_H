Our QMC-MACE model is given by `hydrogen.model` and `cpu_hydrogen.model`, corresponding to the GPU and CPU versions, respectively. The models are identical except that they require different machine architectures to run. The input script used to train the model is given in `input.sh`. For posterity, this script has not been tampered with. In particular, the specified directories have not been changed, so that this script will not properly run unless the proper paths are specified on your particular machine. The training and testing datasets are copied here as `training.xyz` and `testing.xyz`. The output from training is also saved as `output`.

This model was constructed using [MACE](https://github.com/ACEsuit/mace) version 0.2.0. Our complete model is the sum of the MACE model and a pair potential, which we tabulated in `HH.table`. This table is given in LAMMPS' table form.

The python script `calculate_forces.py` provides an example of how our model can be used to calculate forces.
