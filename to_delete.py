import os
import pickle
from matplotlib import pyplot as plt


def pickle_store(filename, item):
    with open(filename, 'wb') as file:
        pickle.dump(item, file)


def pickle_load(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


ranks = pickle_load("results/b21_200_res.rank")
franks = ranks.round()
fmin = int(franks.min())
fmax = int(franks.max())

counters = {key: 0 for key in range(fmin, fmax+1)}
for r in franks:
    counters[int(r)] += 1

print("min_ranks: ", fmin)
print("max_ranks: ", fmax)
print("max count: ", max(counters.values()))
print("min count: ", min(counters.values()))

ranks_values = counters.keys()
ranks_counts = counters.values()

plt.scatter(ranks_values, ranks_counts, c='g', marker='x', label='www')
plt.grid()
plt.xlabel("PageRank")
plt.ylabel("Counts")

plt.yscale("symlog")
plt.xscale("symlog")
plt.legend()
plt.savefig('results/plot.png')

plt.show()
