import logging
import sys
from collections import OrderedDict

import numpy as np

from ..log import log_entry
from .parameter import FittingParameter

logger = logging.getLogger(__name__)


class ComputeArguments:
    r"""Implementation of code to compute energy, forces, and stress.

    This is the base class for other compute arguments. Typically, a user will not
    directly use this.
    """

    implemented_property = []

    def __init__(
        self,
        conf,
        supported_species,
        influence_distance,
        compute_energy=True,
        compute_forces=True,
        compute_stress=False,
    ):
        self.conf = conf
        self.supported_species = supported_species
        self.influence_distance = influence_distance
        self.compute_energy = compute_energy
        self.compute_forces = compute_forces
        self.compute_stress = compute_stress
        self.compute_property = self.check_compute_property()
        self.results = dict([(i, None) for i in self.implemented_property])

    def refresh(self, influence_distance=None, params=None):
        r"""Refresh settings.

        Such as recreating the neighbor list due to the change of cutoff.
        """
        if influence_distance is not None:
            infl_dist = influence_distance
        else:
            try:
                infl_dist = params["influence_distance"].get_value()[0]
            except KeyError:
                report_error('"influence_distance" not provided by "params".')

        self.influence_distance = infl_dist

        # NOTE to be filled
        # create neighbor list based on `infl_dist`

    # TODO also check that the conf provide these properties
    def check_compute_property(self):
        def add_to_compute_property(compute_property, name):
            if name not in self.implemented_property:
                raise NotImplementedError('"{}" not implemented in model.'.format(name))
            compute_property.append(name)

        compute_property = []
        if self.compute_energy:
            add_to_compute_property(compute_property, "energy")
        if self.compute_forces:
            add_to_compute_property(compute_property, "forces")
        if self.compute_stress:
            add_to_compute_property(compute_property, "stress")
        return compute_property

    def compute(self, params):
        r"""Compute the properties required by the compute flags, and store them in
        self.results.

        Parameters
        ----------
        params: dict of 1D array
            Parameters of the model.

        Example
        -------

        energy = a_func_to_compute_energy()
        forces = a_func_to_compute_forces()
        stress = a_func_to_compute_stress()
        self.results['energy'] = energy
        self.results['forces'] = forces
        self.results['stress'] = stress
        """
        # NOTE to be filled
        raise NotImplementedError('"compute" method of "ComputeArguments" not defined.')

    def get_compute_flag(self, name):
        if name in self.compute_property:
            return True
        else:
            return False

    def get_property(self, name):
        if name not in self.compute_property:
            report_error('Model not initialized to comptue "{}".'.format(name))
        result = self.results[name]
        if isinstance(result, np.ndarray):
            result = result.copy()
        return result

    def get_energy(self):
        return self.get_property("energy")

    def get_forces(self):
        return self.get_property("forces")

    def get_stress(self):
        return self.get_property("stress")

    def get_prediction(self):
        if self.compute_energy:
            energy = self.results["energy"]
            pred = np.asarray([energy])
        else:
            pred = np.asarray([])

        if self.compute_forces:
            forces = self.results["forces"]
            pred = np.concatenate((pred, forces.ravel()))

        if self.compute_stress:
            stress = self.results["stress"]
            pred = np.concatenate((pred, stress))

        return pred

    def get_reference(self):
        if self.compute_energy:
            energy = self.conf.energy
            ref = np.asarray([energy])
        else:
            ref = np.asarray([])

        if self.compute_forces:
            forces = self.conf.forces
            ref = np.concatenate((ref, forces.ravel()))

        if self.compute_stress:
            stress = self.conf.stress
            ref = np.concatenate((ref, stress))

        return ref


class Model:
    r"""Base class for all physics-motivated models.

    Typically, a user will not directly use this.

    Parameters
    ----------
    model_name: str (optional)
        Name of the model.

    params_relation_callback: function (optional)
        A callback function to set the relations between parameters, which are
        called each minimization step after the optimizer updates the
        parameters.

        The function with be given the ModelParameters instance as argument, and
        it can use get_value() and set_value() to manipulate the relation
        between parameters.

        Example
        -------

        In the following example, we set the value of B[0] to 2 * A[0].

        def params_relation(params):
            A = params.get_value('A')
            B = params.get_value('B')
            B[0] = 2 * A[0]
            params.set_value('B', B)
    """

    def __init__(self, model_name=None, params_relation_callback=None):
        # TODO params_relation_callbacks may not work for some minimization
        # algorithms since abruptly change the parameter relation may result in
        # loss to go up, then the optimization method can fail. So to a check to
        # implement this only for the minimization methods that support it
        # natively.
        # Update: 2019/07/19
        # This should be fine as long as the dependent parameter is not in the `fitting
        # parameters` vector passed to an optimizer. The dependent parameter can just be
        # thought as a implicit parameter.

        self.model_name = model_name
        if self.model_name is not None:
            self.model_name = self.model_name.rstrip("/")
        self.params_relation_callback = params_relation_callback

        # NOTE to be filled
        self.params = OrderedDict()
        # set up parameters of the calculator
        # e.g.
        # self.params['sigma'] = Parameter(0.5)
        # self.params['epsilon'] = Parameter(0.4)

        # NOTE to be filled
        self.influence_distance = None

        # NOTE to be filled, should a dictionary
        # Key and value are species string and integer code, respectively.
        # if None, it supportes any species
        self.supported_species = None

        # NOTE to be filled
        self.compute_arguments_class = ComputeArguments

        # TODO maybe use metaclass to call this automatically after initialization
        # NOTE do not forget to call this in the subclass
        self.fitting_params = self.init_fitting_params(self.params)

    def write_kim_model(self, path=None):
        # NOTE fill this
        report_error("This model does not support writing to a KIM model.")

    def set_params_relation_callback(self, params_relation_callback):
        r"""Register a function to set the relation between parameters."""
        self.params_relation_callback = params_relation_callback

    def get_influence_distance(self):
        return self.influence_distance

    def get_supported_species(self):
        return self.supported_species

    def get_model_params(self, name):
        r"""Return a copy of the values of parameter.

        Parameters
        ----------
        name: string
            Name of the parameter.
        """
        if name in self.params:
            return self.params[name].get_value()
        else:
            report_error('"{}" is not a parameter of calculator.'.format(name))

    def set_model_params(self, name, value, check_shape=True):
        r"""Update the parameter values.

        Parameters
        ----------
        name: str
            Name of the parameter.

        value: list of floats
            Value of hte parameter.

        check_shape: bool
            If ``True``, check the shape of ``value``.
        """
        if name in self.params:
            self.params[name].set_value(value, check_shape)
        else:
            report_error('"{}" is not a parameter of the model.'.format(name))

    #    def save_model_params(self, path):
    #        params = dict()
    #        for i, j in self.params.items():
    #            v = j.value
    #            if isinstance(v, np.ndarray):
    #                v = v.tolist()
    #            params[i] = v
    #        with open(path, 'w') as fout:
    #            yaml.dump(params, fout, default_flow_style=False)
    #
    #    def load_model_params(self, path):
    #        with open(path, 'r') as fin:
    #            params = yaml.safe_load(fin)
    #        for key, value in params.items():
    #            self.set_model_params(key, value, check_shape=False)

    def echo_model_params(self, path=None):
        r"""Print the optimizable parameters.

        Parameters
        ----------
        path: str (optional)
            Path to print the information. if ``None``, print to stdout.
        """

        if path is not None:
            fout = open(path, "w")
        else:
            fout = sys.stdout

        print(file=fout)
        print("#" + "=" * 80, file=fout)
        print("# Available parameters to optimize.")
        print(file=fout)
        if self.model_name is None:
            name = self.__class__.__name__
        else:
            name = self.model_name
        print("# Model:", name, file=fout)
        print("#" + "=" * 80, file=fout)
        print(file=fout)
        for name, p in self.params.items():
            print("name:", name, file=fout)
            print("value:", p.value, file=fout)
            print("size:", p.size, file=fout)
            print("dtype:", p.dtype, file=fout)
            print("description:", p.description, file=fout)
            print(file=fout)

        if path is not None:
            fout.close()

    def init_fitting_params(self, params):
        return FittingParameter(params)

    def read_fitting_params(self, path):
        self.fitting_params.read(path)

    def set_fitting_params(self, **kwargs):
        self.fitting_params.set(**kwargs)

    def set_one_fitting_param(self, name, settings):
        self.fitting_params.set_one(name, settings)

    #    def save_fitting_params(self, path):
    #        self.fitting_params.save(path)
    #
    #    def load_fitting_params(self, path):
    #        self.fitting_params.load(path)

    def echo_fitting_params(self, path=None):
        self.fitting_params.echo_params(path)

    def get_number_of_opt_params(self):
        return self.fitting_params.get_number_of_opt_params()

    def get_opt_params(self):
        return self.fitting_params.get_opt_params()

    def get_opt_param_name_value_and_indices(self, k):
        return self.fitting_params.get_opt_param_name_value_and_indices(k)

    def has_opt_params_bounds(self):
        return self.fitting_params.has_opt_params_bounds()

    def get_opt_params_bounds(self):
        return self.fitting_params.get_opt_params_bounds()

    def update_fitting_params(self, opt_params):
        r"""Update from optimizer to fitting params."""
        self.fitting_params.update_params(opt_params)

    # TODO if parameters relation set, remove the parameters from fitting params
    # or at least check it is not in the fitting params
    def apply_params_relation(self):
        r"""Force user-specified relation between parameters."""
        if self.params_relation_callback is not None:
            self.params_relation_callback(self.fitting_params)

    def update_model_params(self):
        r"""Update from fitting params to model params."""
        for name, attr in self.fitting_params.params.items():
            self.set_model_params(name, attr["value"], check_shape=False)

    def save(self, path):
        r"""Save a model to disk.

        Parameters
        ----------
        path: str
            Path where to store the model.
        """
        self.fitting_params.save(path)

    def load(self, path):
        r"""Load a model on disk into memory.

        Parameters
        ----------
        path: str
            Path where the model is stored.
        """
        self.fitting_params.load(path)
        self.update_model_params()


class ModelError(Exception):
    def __init__(self, msg):
        super(ModelError, self).__init__(msg)
        self.msg = msg

    def __expr__(self):
        return self.msg


def report_error(msg):
    log_entry(logger, msg, level="error")
    raise ModelError(msg)
