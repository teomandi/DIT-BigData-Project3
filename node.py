from scipy import sparse as sp
import numpy as np


class Node(object):
    def __init__(self, index, key):
        self.index = index
        self.key = key
        self.edges = []
        self.importance = 1
        self.vector = None

    def add_edge(self, e):
        self.edges.append(e)

    def compute_importance(self):
        if len(self.edges) > 0:
            self.importance = 1/len(self.edges)

    def set_vector(self, length, cols, values):
        self.vector = sp.csr_matrix((values, (np.zeros(len(cols)), cols)), shape=(1, length))
