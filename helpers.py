def normalize_path(path):
    index = path.index(0)
    path_ = path[index:] + path[:index]
    if path_[1] > path_[-1]:
        path_[1: len(path_)] = reversed(path_[1: len(path_)])
    return tuple(path_)


def path_length(p, A, n):
    s = 0.0
    for i in range(n):  # [0..n-1]
        s += A[p[i-1], p[i]]  # p[-1] - last element
    return s


def nodes_around(tour, index):
    try:
        around = [(tour[index - 1], index - 1), (tour[index + 1], index + 1)]
    except IndexError:
        around = [(tour[index - 1], index - 1), (tour[0], 0)]
    return around
