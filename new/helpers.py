def adjacency_list(E, reversed_order=False):
    E_ = {}
    for s1, s2 in E:
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
    index1 = tour.index(edge[0])
    index2 = tour.index(edge[1])
    return index1 == index2 + 1 or index1 == index2 - 1


def nodes_around(tour, index):
    succ = index + 1
    if succ == len(tour):
        succ = 0
    return [(tour[index - 1], index - 1), (tour[succ], succ)]


def check_tour(tour, broken, joined):
    # long, ugly implementation, many ifs, but efficient - average O(n), where n is tour length
    adjacent = {}
    adjacent[tour[-1]] = [tour[0]]
    adjacent[tour[0]] = [tour[-1]]
    for index in range(1, len(tour)-1):
        adjacent[tour[index]] = [tour[index-1]]
        adjacent[tour[index-1]].append(tour[index])
    adjacent[tour[-1]].append(tour[-2])
    adjacent[tour[-2]].append(tour[-1])

    for v1, v2 in broken:
        if v2 in adjacent[v1] and v1 in adjacent[v2]:
            adjacent[v1].remove(v2)
            adjacent[v2].remove(v1)
        else:
            return False, None

    for v1, v2 in joined:
        if v2 not in adjacent[v1] and v1 not in adjacent[v2]:
            adjacent[v1].append(v2)
            adjacent[v2].append(v1)
        else:
            return False, None

    node = 0
    new_tour = [0]
    for index in range(len(tour)):
        if node not in adjacent.keys():
            return False, None

        possible_nodes = adjacent[node]
        if len(possible_nodes) != 2:
                return False, None

        if index == 0:
            next_node = min(possible_nodes)
            new_tour.append(next_node)
            del adjacent[node]
            node = next_node

        elif index == len(tour)-1:
            if possible_nodes[0] == 0 or possible_nodes[1] == 0:
                return True, new_tour

        else:
            if possible_nodes[0] == new_tour[index-1]:
                next_node = possible_nodes[1]
            else:
                next_node = possible_nodes[0]
            new_tour.append(next_node)
            del adjacent[node]
            node = next_node

    return False, None


