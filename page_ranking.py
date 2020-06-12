import numpy as np
import time
import pickle
import os
from node import Node
from matplotlib import pyplot as plt

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

    def simple_iterate(self, iter):
        iter_tm = time.time()
        p = self.rank.copy()
        for idx, src in enumerate(self.graph):
            self.rank[self.graph[src].index] = (self.graph[src].vector * p)[0]
        print(iter, ") Iteration took {:.3f}".format(time.time() - iter_tm))

    def improved_iterate(self, iter):
        iter_tm = time.time()
        a = 0.85
        na = (1 - a) * np.ones(self.length)
        p = self.rank.copy()
        for idx, src in enumerate(self.graph):
            self.rank[self.graph[src].index] = (self.graph[src].vector * p)[0]
        self.rank = a * self.rank + na
        print(iter, ") Iteration took {:.3f}".format(time.time() - iter_tm))

    # weight = 1 : The bottom 20
    # weight = -1 : The top 20
    def top(self, n, weight=1):
        return [(idx, self.rank[idx]) for idx in (weight*self.rank).argsort()[:n]]

    def reset(self):
        self.rank = np.ones(self.length)

    def create_plot(self, store_path):
        franks = self.rank.round()
        fmin = int(franks.min())
        fmax = int(franks.max())
        counters = {key: 0 for key in range(fmin, fmax + 1)}
        for r in franks:
            counters[int(r)] += 1
        ranks_values = counters.keys()
        ranks_counts = counters.values()
        plt.scatter(ranks_values, ranks_counts, c='g', marker='x', label='www')
        plt.grid()
        plt.xlabel("PageRank")
        plt.ylabel("Counts")
        plt.yscale("symlog")
        plt.xscale("symlog")
        plt.legend()
        plt.savefig(store_path)

    def store_top_results(self, N, w, store_path):
        results = self.top(N, w)
        f = open(store_path, 'w')
        f.write("nodeId,rank\n")
        for (node_id, rank) in results:
            f.write(str(node_id) + "," + str(rank) + "\n")
        f.close()


def evaluate():
    starting_tm = time.time()
    graph_path = "web-Google.txt"
    # graph_path = "example-graph.txt"
    iterations = [10, 50, 100, 200]
    if not os.path.isdir("results"):
        os.mkdir("results")
    ranks_dir = os.path.join("results", "ranks")
    plots_dir = os.path.join("results", "plots")
    results_dir = os.path.join("results", "results")

    if not os.path.isdir(ranks_dir):
        os.mkdir(ranks_dir)
    if not os.path.isdir(plots_dir):
        os.mkdir(plots_dir)
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)
    # method:
    method = "simple"
    a = 1
    pagerank = PageRanker(graph_path, method)
    for i in range(iterations[-1]):
        pagerank.iterate(i)
        if i+1 in iterations:
            pagerank.store_top_results(20, -1, os.path.join(results_dir, method+str(a)+"_"+str(i)+"_top20.txt"))
            pagerank.store_top_results(20, 1, os.path.join(results_dir, method+str(a)+"_"+str(i)+"_bottom20.txt"))
            pagerank.create_plot(os.path.join(results_dir, method+str(a)+"_"+str(i)+".png"))
            print("Results stored for i: ", )
            print(i+1, ") Done took {:.3f}".format(time.time() - starting_tm))


if __name__ == '__main__':
    evaluate()
