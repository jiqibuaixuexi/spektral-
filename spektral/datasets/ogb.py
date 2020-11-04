import numpy as np
import scipy.sparse as sp

from spektral.data import Dataset, Graph


class OGB(Dataset):
    """
    Wrapper for OGB datasets.

    **Arguments**

    - `dataset`: an OGB library-agnostic Graph*Dataset object.

    """
    def __init__(self, dataset, **kwargs):
        self.dataset = dataset
        super().__init__(**kwargs)

    def read(self):
        if len(self.dataset) > 1:
            return [Graph(*_elem_to_numpy(elem)) for elem in self.dataset]
        else:
            # OGB crashed if we try to iterate over a NodePropPredDataset
            return [Graph(*_elem_to_numpy(self.dataset[0]))]


def _elem_to_numpy(elem):
    graph, label = elem
    n = graph['num_nodes']
    x = graph['node_feat']
    row, col = graph['edge_index']
    a = sp.coo_matrix((np.ones_like(row), (row, col)), shape=(n, n))
    e = graph['edge_feat']

    return x, a, e, label
