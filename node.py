class Node(object):
    def __init__(self, key, first_edge):
        self.key = key
        self.edges = [first_edge]
        self.importance = 1

    def add_edge(self, e):
        self.edges.append(e)

    def compute_importance(self):
        self.importance = 1/len(self.edges)
