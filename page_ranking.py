import numpy as np
import time
import pickle
import os
from node import Node
from matplotlib import pyplot as plt
import argparse


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
        self.nodeset = []
        print("Parsing the Graph file")
        init_tm = time.time()
        with open(graph_file_path) as fp:
            line = fp.readline()
            while line:
                if "#" in line:
                    print("Found comment: ", line[:-1])
                    line = fp.readline()  # in the end
                    continue
                src, dest = [int(i) for i in line.split()]
                if src not in self.graph:
                    self.nodeset.append(src)
                    self.graph[src] = Node(len(self.nodeset)-1, src)
                if dest not in self.graph:
                    self.nodeset.append(dest)
                    self.graph[dest] = Node(len(self.nodeset)-1, dest)
                self.graph[src].add_edge(self.graph[dest])
                line = fp.readline()  # in the end
        # sets variables
        self.length = len(self.nodeset)
        self.rank = np.ones(self.length)
        # some prints
        print("Parse took {:.3f}".format(time.time() - init_tm))
        print("nodes: ", self.length)
        print("graph: ", len(self.graph))
        print("Calculating the importance of each node")
        init_tm = time.time()
        for _key in self.graph:
            self.graph[_key].compute_importance()
        print("Importance took {:.3f}".format(time.time() - init_tm))
        # calculates the vector for each node
        print("Creating the vectors of each node")
        vector_tm = time.time()
        for _key in self.graph:
            values = []
            cols = []
            for dest in self.graph[_key].edges:
                cols.append(dest.index)
                values.append(dest.importance)
            self.graph[_key].set_vector(self.length, cols, values)
        print("Vectorizing took {:.3f}".format(time.time() - vector_tm))

    def simple_iterate(self, iter, a=None, convergence=False, tol=1.96e-6):
        iter_tm = time.time()
        p = self.rank.copy()
        for idx, src in enumerate(self.graph):
            self.rank[self.graph[src].index] = (self.graph[src].vector * p)[0]
        print(iter, ") Iteration took {:.3f}".format(time.time() - iter_tm))
        if convergence:
            err = sum([abs(p[i] - self.rank[i]) for i in range(self.length)])
            if err < self.length * tol:
                print("It converged on iter :", iter, "!!!")
                return True
        return False

    def improved_iterate(self, iter, a=0.85, convergence=False, tol=1.96e-6):
        iter_tm = time.time()
        na = (1 - a) * np.ones(self.length)
        p = self.rank.copy()
        for idx, src in enumerate(self.graph):
            self.rank[self.graph[src].index] = (self.graph[src].vector * p)[0]
        self.rank = a * self.rank + na
        print(iter, ") Iteration took {:.3f}".format(time.time() - iter_tm))
        if convergence:
            err = sum([abs(p[i] - self.rank[i]) for i in range(self.length)])
            if err < self.length * tol:
                print("It converged on iter :", iter, "!!!")
                return True
        return False

    # weight = 1 : The bottom 20
    # weight = -1 : The top 20
    def top(self, n, weight=1):
        return [(self.nodeset[idx], self.rank[idx]) for idx in (weight*self.rank).argsort()[:n]]

    def reset(self):
        self.rank = np.ones(self.length)

    def create_plot(self, store_path, idx, normalized=True):
        print("Creating plot at ", store_path)
        if normalized:
            franks = np.ceil(self.rank)
            (ranks_values, ranks_counts) = np.unique(franks, return_counts=True)
            print("ranks_counts: ", len(ranks_counts), "ranks_values: ", len(ranks_values))
            # print("Counts: ", ranks_counts)
            # print("Values: ", ranks_values)
            if ranks_values[0] == 0:
                ranks_values[0] = 1  # <----
        else:
            (ranks_values, ranks_counts) = np.unique(self.rank, return_counts=True)
            print("ranks_counts: ", ranks_counts.shape, "ranks_values: ", ranks_values.shape)
        plt.figure(idx)
        plt.scatter(ranks_values, ranks_counts, c='b', marker='x', label='www')
        plt.grid()
        plt.xlabel("PageRank")
        plt.ylabel("Counts")
        plt.yscale("log")
        plt.xscale("log")  # symlog
        plt.legend()
        plt.savefig(store_path)

    def store_top_results(self, N, w, store_path):
        results = self.top(N, w)
        f = open(store_path, 'w')
        f.write("nodeId,rank\n")
        for (node_id, rank) in results:
            f.write(str(node_id) + "," + str(rank) + "\n")
        f.close()


def make_dirs():
    res_d = "results"
    if not os.path.isdir(res_d):
        os.mkdir(res_d)
    ranks_dir = os.path.join(res_d, "ranks")
    plots_dir = os.path.join(res_d, "plots")
    results_dir = os.path.join(res_d, "results")
    if not os.path.isdir(ranks_dir):
        os.mkdir(ranks_dir)
    if not os.path.isdir(plots_dir):
        os.mkdir(plots_dir)
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)
    return ranks_dir, plots_dir, results_dir


def evaluate(graph_path, method, a=None):
    print("Evaluate starts")
    if method == "simple":
        a = ""  # for the file names
    starting_tm = time.time()
    iterations = [10, 50, 100, 200]
    ranks_dir, plots_dir, results_dir = make_dirs()
    pagerank = PageRanker(graph_path, method)
    for i in range(iterations[-1]):
        pagerank.iterate(i, a)
        if i+1 in iterations:
            pagerank.store_top_results(20, -1, os.path.join(results_dir, method+str(a)+"_"+str(i+1)+"_top20.txt"))
            pagerank.store_top_results(20, 1, os.path.join(results_dir, method+str(a)+"_"+str(i+1)+"_bottom20.txt"))
            pagerank.create_plot(os.path.join(plots_dir, method+str(a)+"_"+str(i+1)+".png"), i+1)
            print("Iteration results stored (", i+1, ") Done took {:.3f}".format(time.time() - starting_tm))


def eval_converge(graph_path, method, a=None):
    print("Converge starts")
    pagerank = PageRanker(graph_path, method)
    iter = 0
    while True:
        if pagerank.iterate(iter, a, convergence=True):
            break
        iter += 1
    print("converged into: ", iter)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Page Rank. Project 3 Big-Data 2020',
        epilog='Enjoy the program! :)'
    )
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        help="The path for the .txt file with the Graph",
        required=True
    )
    parser.add_argument(
        '-m',
        '--method',
        type=str,
        help='Selected method for PageRanking. Accepted Options are \'simple\', \'improved\'',
        action='store',
        required=True
    )
    parser.add_argument(
        '-a',
        '--a',
        type=float,
        help='a is numeric value',
        action='store',
    )
    parser.add_argument(
        '-i',
        '--iterations',
        type=int,
        help='How many iterations the program to perform. On evaluation it is not required',
        action='store'
    )
    parser.add_argument(
        '-c',
        '--converge',
        help="Enables the convergence functionality",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '-e',
        '--eval',
        help="Performs evaluations",
        default=False,
        action='store_true'
    )
    args = parser.parse_args()
    arguments = vars(args)
    print("Given args: ", arguments)

    if arguments['method'] == "improved":
        if arguments['a'] is None:
            print("Error: a value is not set")
            exit()
    if arguments["eval"]:
        evaluate(arguments["path"], arguments["method"], arguments["a"])
    elif arguments["converge"]:
        eval_converge(arguments["path"], arguments["method"], arguments["a"])
    else:
        if arguments['iterations'] is None:
            print("Error: No iterations mentioned")
            exit()
        starting_tm = time.time()
        ranks_dir, plots_dir, results_dir = make_dirs()
        pagerank = PageRanker(arguments["path"], arguments["method"])
        for i in range(arguments["iterations"]):
            pagerank.iterate(i, arguments['a'])
        if arguments["a"] is None:
            arguments["a"] = ""
        pagerank.store_top_results(20, -1,
                                   os.path.join(
                                       results_dir,
                                       arguments["method"] + str(arguments["a"]) +
                                       "_" + str(arguments["iterations"]) + "_top20.txt")
                                   )
        pagerank.store_top_results(20, 1,
                                   os.path.join(
                                       results_dir,
                                       arguments["method"] + str(arguments["a"]) +
                                       "_" + str(arguments["iterations"]) + "_bottom20.txt"))
        pagerank.create_plot(
            os.path.join(plots_dir, arguments["method"] + str(arguments["a"]) +
                         "_" + str(arguments["iterations"]) + ".png"), arguments["iterations"]
        )
        print("Iteration results stored (", arguments["iterations"],
              ") Done took {:.3f}".format(time.time() - starting_tm))
