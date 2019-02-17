import numpy as np
import pickle


def save_TSP(A, n, nodes_array, file_name):
    with open(file_name + '.matrix', "wb") as fh:
        pickle.dump((A, n, nodes_array), fh)


def load_TSP(file_name):
    with open(file_name, "rb") as fh:
        (A, n, nodes_array) = pickle.load(fh)
        return A, n, nodes_array


def save_LON(V, E, A, n, nodes_array, file_name):
    # graph: A - adjacency matrix with weights, n - dimensions
    # landscape: V - optima vertices, E - escape edges
    with open(file_name, "wb") as fh:
        pickle.dump((V, E, A, n, nodes_array), fh)


def load_LON(file_name):
    with open(file_name, "rb") as fh:
        (V, E, A, n, nodes_array) = pickle.load(fh)
        return V, E, A, n, nodes_array


def save_metrics(metrics_tuple, file_name):
    with open(file_name, "wb") as fh:
        pickle.dump(metrics_tuple, fh)


def load_metrics(file_name):
    with open(file_name, "rb") as fh:
        metrics_tuple = pickle.load(fh)
        return metrics_tuple


def parse_TSP_from_file(filename):
    with open(filename) as fh:
        data = fh.read().split("\n")  # lines of input file
    n = int(data[3].split()[1])  # dimensions (number of nodes)
    A = np.empty((n, n), dtype=int)  # adjacency matrix with weights

    for i in range(n):
        edges = map(int, data[i + 8].split())  # map(function, iterables), int(string, base)
        for j, v in enumerate(edges):
            A[i, j] = v

    return A, n

