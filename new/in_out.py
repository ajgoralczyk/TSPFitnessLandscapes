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


def save_best(file_name, best_path_length, best_path):
    with open(file_name, "wb") as fh:
        pickle.dump(tuple([best_path_length, best_path]), fh)

def load_best(file_name):
    with open(file_name, "rb") as fh:
        metrics_tuple = pickle.load(fh)
        return metrics_tuple


def parse_TSP_from_file(filename):
    data = ""
    with open(filename) as fh:
        data = fh.read().split("\n")
    n = int(data[3].split()[-1])
    e_type = data[4].split()[-1]
    e_format = ""
    if e_type == "EXPLICIT":
        e_format = data[5].split()[-1]

    A = np.empty((n, n), dtype=int)
    if e_type == "EXPLICIT" and e_format == "UPPER_ROW":
        for i in range(n - 1):
            edges = map(int, data[i + 8].split())
            for j, v in enumerate(edges):
                A[i, i + j + 1] = v
                A[i + j + 1, i] = v
        for i in range(n):
            A[i, i] = 0

    if e_type == "EXPLICIT" and e_format == "FULL_MATRIX":
        for i in range(n):
            edges = map(int, data[i + 8].split())
            for j, v in enumerate(edges):
                A[i, j] = v
    if e_type == "EUC_2D":
        coords = np.empty((n, 2))
        for i in range(n):
            coord = list(map(int, data[i + 6].split()))
            coords[coord[0] - 1, :] = np.array([coord[1:]])
        for i in range(n):
            for j in range(n):
                A[i, j] = np.sqrt(((coords[i, :] - coords[j, :]) ** 2).sum())
    return A, n
