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
    def __init__(self, graph_file_path):
        self.graph = {}
        self.nodeset = set()

        init_tm = time.time()
        with open(graph_file_path) as fp:

            line = fp.readline()
            while line:
                if "#" in line:
                    print("comment: ", line[:-1])
                    line = fp.readline()  # in the end
                    continue
                src, dest = [int(i) for i in line.split()]
                self.nodeset.add(src)
                self.nodeset.add(dest)

                if src not in self.graph:
                    self.graph[src] = Node(src, dest)
                else:
                    self.graph[src].add_edge(dest)

                line = fp.readline()  # in the end
        self.nodeset = list(self.nodeset)
        print("Init took {:.3f}".format(time.time() - init_tm))
        print("nodes: ", len(self.nodeset))
        print("graph: ", len(self.graph))
        init_tm = time.time()
        for _key in self.graph:
            self.graph[_key].compute_importance()
        print("Importance took {:.3f}".format(time.time() - init_tm))
        self.rank = np.ones(len(self.nodeset))

    def iterate(self):
        iter_tm = time.time()
        p = self.rank.copy()
        for src in self.graph:
            s = 0
            for dest in self.graph[src].edges:
                if dest in self.graph:
                    # print(
                    #   self.nodeset.index(src), ") ",
                    #   self.graph[dest].importance, " * ", p[self.nodeset.index(dest)]
                    # )
                    s += self.graph[dest].importance * p[self.nodeset.index(dest)]
            self.rank[self.nodeset.index(src)] = s
            # print("---  *  ---")
        print("Iteration took {:.3f}".format(time.time() - iter_tm))

    # weight = 1 : The bottom 20
    # weight = -1 : The top 20
    def top(self, n, weight=1):
        return [self.rank[i] for i in (weight*self.rank).argsort()[:20]]


if __name__ == '__main__':
    # path = "example-graph.txt"
    path = "web-Google.txt"

    pr = PageRanker(path)
    for i in range(2):
        pr.iterate()
    print("Top 20: ", pr.top(20, -1))
    print("Bottom 20: ", pr.top(20, 1))




