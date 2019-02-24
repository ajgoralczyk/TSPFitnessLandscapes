def adjacency_list(V, E, reversed_order=False):
    E_ = {}
    for s1, s2 in E:
        if s1 in V and s2 in V:  # TODO in my cases should never be false
            if not reversed_order:
                if s1 in E_:
                    E_[s1].append(s2)
                else:
                    E_[s1] = [s2]
            else:
                if s2 in E_:
                    E_[s2].append(s1)
                else:
                    E_[s2] = [s1]
    return E_


def path_length(p, A, n):
    s = 0.0
    for i in range(n):  # [0..n-1]
        s += A[p[i-1], p[i]]  # p[-1] - last element
    return s


def make_pair(i, j):
    if i > j: return (j, i)
    else: return (i, j)


def tour_contains(tour, edge):
    index = tour.index(edge[0])
    return tour.index(edge[1]) == index + 1


def nodes_around(tour, node):
    index = tour.index(node)
    succ = index + 1
    if succ == len(tour):
        succ = 0
    return (tour[index - 1], tour[succ])


def check_tour(tour, broken, joined):
    edges_in_tour = set()
    for i in range(len(tour)):
        edges_in_tour.add(make_pair(tour[i - 1], tour[i]))
    edges = (edges_in_tour - broken) | joined

    if len(edges) < len(tour): return False, []

    node = 0
    new_tour = [0]

    while len(edges) > 0:
        for i, j in edges:
            if i == node:
                new_tour.append(j)
                node = j
                break
            elif j == node:
                new_tour.append(i)
                node = i
                break
        edges.remove((i, j))

    return len(new_tour) == len(tour), new_tour



# TODO
# neighbours 
# porównać implementacje z algorytmem z 1998


# dodać zapisywanie najlepszego
# początkowe local optima


# sprawdzić czy się nie wywala

















