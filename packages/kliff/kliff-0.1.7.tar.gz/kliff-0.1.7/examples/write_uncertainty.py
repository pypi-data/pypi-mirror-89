"""
.. _tut_nn:

Train a neural network potential
================================

In this tutorial, we train a neural network (NN) potential for silicon

"""


##########################################################################################
# We are going to fit the NN potential to a training set of energies and forces from
# compressed and stretched diamond silicon structures (the same training set used in
# :ref:`tut_kim_sw`).
# Download the training set :download:`Si_training_set.tar.gz <https://raw.githubusercontent.com/mjwen/kliff/master/examples/Si_training_set.tar.gz>`
# and extract the tarball: ``$ tar xzf Si_training_set.tar.gz``.
# The data is stored in **extended xyz** format, and see :ref:`doc.dataset` for more
# information of this format.
#
# .. warning::
#     The ``Si_training_set`` is just a toy data set for the purpose to demonstrate how to
#     use KLIFF to train potentials. It should not be used to train any potential for real
#     simulations.
#
# Let's first import the modules that will be used in this example.

import torch

from kliff import nn
from kliff.calculators import CalculatorTorch
from kliff.dataset import Dataset
from kliff.descriptors import SymmetryFunction
from kliff.models import NeuralNetwork

##########################################################################################
# Model
# -----
#
# For a NN model, we need to specify the descriptor that transforms atomic environment
# information to the fingerprints, which the NN model uses as the input. Here, we use the
# symmetry functions proposed by Behler and coworkers.

descriptor = SymmetryFunction(
    cut_name="cos", cut_dists={"Si-Si": 5.0}, hyperparams="set51", normalize=True
)


##########################################################################################
# The ``cut_name`` and ``cut_dists`` tell the descriptor what type of cutoff function to
# use and what the cutoff distances are. ``hyperparams`` specifies the set of
# hyperparameters used in the symmetry function descriptor. If you prefer, you can provide
# a dictionary of your own hyperparameters. And finally, ``normalize`` informs that the
# generated fingerprints should be normalized by first subtracting the mean and then
# dividing the standard deviation. This normalization typically makes it easier to
# optimize NN model.
#
# We can then build the NN model on top of the descriptor.

N1 = 10
N2 = 10
model = NeuralNetwork(descriptor)
model.add_layers(
    # first hidden layer
    nn.Linear(descriptor.get_size(), N1),
    nn.Tanh(),
    nn.Dropout(p=0.1),
    # second hidden layer
    nn.Linear(N1, N2),
    nn.Tanh(),
    nn.Dropout(p=0.1),
    # output layer
    nn.Linear(N2, 1),
)
model.set_save_metadata(prefix="./kliff_saved_model", start=5, frequency=2)
model.load("final_model.pkl", mode="train")  # mode == 'train' because we need dropout

##########################################################################################
# In the above code, we build a NN model with an input layer, two hidden layer, and an
# output layer. The ``descriptor`` carries the information of the input layer, so it is
# not needed to be specified explicitly. For each hidden layer, we first do a linear
# transformation using ``nn.Linear(size_in, size_out)`` (essentially carrying out :math:`y
# = xW+b`, where :math:`W` is the weight matrix of size ``size_in`` by ``size_out``, and
# :math:`b` is a vector of size ``size_out``. Then we apply the hyperbolic tangent
# activation function ``nn.Tanh()`` to the output of the Linear layer (i.e. :math:`y`) so
# as to add the nonlinearity. We use a Linear layer for the output layer as well, but
# unlike the hidden layer, no activation function is applied here. The input size
# ``size_in`` of the first hidden layer must be the size of the descriptor, which is
# obtained using ``descriptor.get_size()``. For all other layers (hidden or output), the
# input size must be equal to the output size of the previous layer. The ``out_size`` of
# the output layer must be 1 such that the output of the NN model gives the energy of the
# atom.
#
# The ``set_save_metadata`` function call informs where to save intermediate models during
# the optimization (discussed below), and what the starting epoch and how often to save
# the model.
#
#
# Training set and calculator
# ---------------------------
#
# The training set and the calculator are the same as explained in :ref:`tut_kim_sw`. The
# only difference is that we need to use the
# :mod:`~kliff.calculators.CalculatorTorch()`, which is targeted for the NN model.
# Also, its ``create()`` method takes an argument ``reuse`` to inform whether to reuse the
# fingerprints generated from the descriptor if it is present.

# training set
dataset_name = "Si_training_set/varying_alat"
tset = Dataset()
tset.read(dataset_name)
configs = tset.get_configs()

# calculator
calc = CalculatorTorch(model)
calc.create(
    configs,
    reuse=True,
    fingerprints_path="fingerprints.pkl",
    fingerprints_mean_and_stdev_path="fingerprints_mean_and_stdev.pkl",
)


##########################################################################################
# Loss function
# -------------
#
# KLIFF uses a loss function to quantify the difference between the training data and
# potential predictions and uses minimization algorithms to reduce the loss as much as
# possible. In the following code snippet, we create a loss function that uses the
# ``Adam`` optimizer to minimize it. The Adam optimizer supports minimization using
# `mini-batches` of data, and here we use ``100`` configurations in each minimization step
# (the training set has a total of 400 configurations as can be seen above), and run
# through the training set for ``10`` epochs. The learning rate ``lr`` used here is
# ``0.001``, and typically, one may need to play with this to find an acceptable one that
# drives the loss down in a reasonable time.


def nll(v, ref, var):
    var = var.clone().detach()  # make var not dependent on model parameters
    min_var = 1e-20 * torch.ones(len(var))
    var = torch.max(var, min_var)
    rst = torch.log(var) + (v - ref) ** 2 / var
    rst = torch.sum(rst)
    return rst


def loss_fn(e, ref_e, var_e, f, ref_f, var_f, f_weight, batch_size=100):
    return 1 / batch_size * (nll(e, ref_e, var_e) + f_weight * nll(f, ref_f, var_f))


eval_times = 5
BATCH_SIZE = 1

dataloader = calc.get_compute_arguments(batch_size=BATCH_SIZE)


for batch in dataloader:

    def closure():

        e_ref = torch.stack([sample["energy"] for sample in batch])
        f_ref = torch.cat([sample["forces"].reshape(-1) for sample in batch])

        energies = []
        forces = []

        for i in range(eval_times):
            results = calc.compute(batch)
            energy_batch = results["energy"]
            forces_batch = results["forces"]
            energies.append(torch.stack(energy_batch))
            forces.append(torch.cat(forces_batch))

        energies = torch.stack(energies)
        forces = torch.stack(forces)
        e_mean, e_var = torch.var_mean(energies, dim=0)
        f_mean, f_var = torch.var_mean(forces, dim=0)
        loss = loss_fn(
            e_mean,
            e_ref,
            e_var,
            f_mean,
            f_ref,
            f_var,
            f_weight=0.001,
            batch_size=BATCH_SIZE,
        )

        return loss

    loss = float(closure())
    print(loss)
