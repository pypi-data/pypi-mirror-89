from .plotting_functions.plot_alignment import pl_cytopath_alignment
from .plotting_functions.plot_sampling import pl_cytopath_sampling

def plot_alignment(data, directory='', basis='', name='', size=10, figsize=(12,3), smoothing=False):
    pl_cytopath_alignment(data, folder=directory, basis=basis, key=name, size=size, figsize=figsize, smoothing=smoothing)

def plot_sampling(data, directory='', basis=''):
    pl_cytopath_sampling(data, folder=directory, basis=basis)