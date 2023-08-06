import networkx as nx
import pyscipopt as scip

from geco.mips.independent_set.generic import independent_set


def sun_params(n, m, seed=0):
    return nx.generators.barabasi_albert_graph(n, m, seed)


def sun_instance(n, m, seed=0):
    """
    Generates a maximum independent set instance as described in [1].

    Parameters
    ----------
    n: int
        number of nodes.
    m: int
        edge probability
    seed: int, random state or None
        randomization seed

    Returns
    -------
    model: scip.Model
        pyscipopt model of the instance.

    References
    ----------
    .. [1] Haoran Sun, Wenbo Chen, Hui Li, & Le Song (2021).
         Improving Learning to Branch via Reinforcement Learning. In Submitted to
         International Conference on Learning
    """
    return independent_set(sun_params(n, m, seed), name="Sun Independent Set")


def expand_sun_params():
    pass
