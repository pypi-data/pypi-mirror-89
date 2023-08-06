import numpy as np
from geco.mips.facility_location.generic import capacitated_facility_location
from geco.mips.facility_location.cornuejols import *
from networkx.utils import py_random_state


def sun_instance(n_customers, n_facilities, ratio, seed=0):
    return cornuejols_instance(n_customers, n_facilities, ratio, seed)


def sun_instance_params(n_customers, n_facilities, ratio, seed):
    """Implements the generation techniques used in [1].

     References
    ----------
    .. [1] Haoran Sun, Wenbo Chen, Hui Li, & Le Song (2021).
         Improving Learning to Branch via Reinforcement Learning. In Submitted to
         International Conference on Learning
    """
    return cornuejols_instance_params(n_customers, n_facilities, ratio, seed)


@py_random_state(-1)
def expand_sun_instance_params(new_params, base_result, seed=0):
    n_customers, *_ = new_params
    trans_costs, demands, fixed_costs, capacities = base_result
