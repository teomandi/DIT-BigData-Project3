import scipy.sparse as sp
import numpy as np
import time
import pickle
from node import Node


def pickle_store(filename, item):
    with open(filename, 'wb') as file:
        pickle.dump(item, file)


def pickle_load(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


class PageRanker(object):
    def __init__(self, graph_file_path, method):
        if method == "simple":
            self.iterate = self.simple_iterate
        elif method == "improved":
            self.iterate = self.improved_iterate
        else:
            print("Error: unknown method")
            return
        self.graph = {}
        self.nodeset = set()
        # parsing the node file
        init_tm = time.time()
        with open(graph_file_path) as fp:
            line = fp.readline()
            while line:
                if "#" in line:
                    print("Found comment: ", line[:-1])
                    line = fp.readline()  # in the end
                    continue
                src, dest = [int(i) for i in line.split()]
                self.nodeset.add(src)
                if src not in self.graph:
                    self.graph[src] = Node(len(self.nodeset)-1, src)
                self.nodeset.add(dest)
                if dest not in self.graph:
                    self.graph[dest] = Node(len(self.nodeset)-1, dest)
                self.graph[src].add_edge(self.graph[dest])
                line = fp.readline()  # in the end
        # sets variables
        self.nodeset = list(self.nodeset)
        self.length = len(self.nodeset)
        self.rank = np.ones(self.length)
        # some prints
        print("Init took {:.3f}".format(time.time() - init_tm))
        print("nodes: ", self.length)
        print("graph: ", len(self.graph))
        # computes the importance for each node
        init_tm = time.time()
        for _key in self.graph:
            self.graph[_key].compute_importance()
        print("Importance took {:.3f}".format(time.time() - init_tm))
        # calculates the vector for each node
        vector_tm = time.time()
        for _key in self.graph:
            values = []
            cols = []
            for dest in self.graph[_key].edges:
                cols.append(dest.index)
                values.append(dest.importance)
            self.graph[_key].set_vector(self.length, cols, values)
        print("Vector took {:.3f}".format(time.time() - vector_tm))

    def simple_iterate(self):
        iter_tm = time.time()
        p = self.rank.copy()
        for idx, src in enumerate(self.graph):
            self.rank[self.graph[src].index] = (self.graph[src].vector * p)[0]
        print("Iteration took {:.3f}".format(time.time() - iter_tm))

    def improved_iterate(self):
        iter_tm = time.time()
        a = 0.2
        na = (1 - a) * np.ones(self.length)
        p = self.rank.copy()
        for idx, src in enumerate(self.graph):
            self.rank[self.graph[src].index] = (self.graph[src].vector * p)[0]
        self.rank = a * self.rank + na
        print("Iteration took {:.3f}".format(time.time() - iter_tm))

    # weight = 1 : The bottom 20
    # weight = -1 : The top 20
    def top(self, n, weight=1):
        return [(idx, self.rank[idx]) for idx in (weight*self.rank).argsort()[:n]]


if __name__ == '__main__':
    starting_tm = time.time()

    # path = "example-graph.txt"
    path = "web-Google.txt"
    iterations = 10
    N = 20
    # method = "simple"
    method = "improved"

    pr = PageRanker(path, method)
    for i in range(iterations):
        pr.iterate()

    t20 = pr.top(N, -1)
    f = open('results/b12_top20.txt', 'w')
    f.write("nodeId,rank\n")
    for (node_id, rank) in t20:
        f.write(str(node_id) + "," + str(rank) + "\n")
    f.close()

    b20 = pr.top(N, 1)
    f = open('results/b12_bottom20.txt', 'w')
    f.write("nodeId,rank\n")
    for (node_id, rank) in b20:
        f.write(str(node_id) + "," + str(rank) + "\n")
    f.close()

    print("Done took {:.3f}".format(time.time() - starting_tm))




