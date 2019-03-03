from helpers import *
# import datetime

def optimise_path(path, A, n): # Step 1
    solutions = set()
    intersection = set()
    previous_edges = set()
    better = True
    i = 1

    while better:
        better, better_path, better_path_length = improve(solutions, intersection, path, A, n)
        solutions.add(tuple(better_path))

        if len(previous_edges) == 0:
            for index in range(len(better_path)):
                previous_edges.add(make_pair(better_path[index - 1], better_path[index]))
        elif len(intersection) == 0:
            edges = set()
            for index in range(len(better_path)):
                edges.add(make_pair(better_path[index - 1], better_path[index]))
            intersection = previous_edges & edges
        else:
            edges = set()
            for index in range(len(better_path)):
                edges.add(make_pair(better_path[index - 1], better_path[index]))
            intersection = intersection & edges

        path = better_path
        i += 1

    return path

def improve(solutions, intersection, path, A, n):
    for t1, index_t1 in enumerate(path):  # Step 2, 12
        around_t1 = nodes_around(path, index_t1) # TODO in: path, index   out: ((node1, index1),(node2, index2))

        for t2, index_t2 in around_t1:  # Step 3, 11
            broken = {make_pair(t1, t2)}
            gain = A[t1, t2]
            closest_neighbours = closest(A, t2, path, gain, broken)

            for t3, (_, Gi, index_t3) in closest_neighbours:
                if t3 not in around_t1: # TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    joined = {make_pair (t2, t3)}  # Rule 1 - only sequential exchanges

                    is_better, better_path, better_path_cost = chooseX(solutions, intersection, A, n, path, t1, t3, Gi, broken, joined)
                    if is_better:
                        return is_better, better_path, better_path_cost

    return False, path, None  # Step 13

def closest(A, t2i, tour, gain, broken): # out: { node : [priority, new gain, index(node)] }
    distances = []
    for index, node in enumerate(tour):
        if node == t2i:
            continue
        distances.append(tuple([node, A[t2i, node], index]))
    neighbours = sorted(distances, key=lambda tup: tup[1])[:5]  # Rule 5 - 5 closest neighbours

    closest_neighbours = {}
    for node in neighbours:
        yi = make_pair(t2i, node[0])
        new_gain = gain - node[1]  # Rule 2 - selecting yi, that Gi (g1 + g2 + ... + gi) > 0

        if new_gain > 0 and yi not in broken and not tour_contains(tour, yi):  # Rule 4 - X, Y separate
            for next_node in nodes_around(tour, node[0]): # TODO in: path, index   out: ((node1, index1),(node2, index2))
                xi = make_pair(node[0], next_node)

                if xi not in broken:
                    diff = A[node[0], next_node] - A[t2i, node[0]] # Rule 8 - selecting yi with priority c(xi+1) - c(yi)

                    if node[0] in closest_neighbours and diff > closest_neighbours[node[0]][0]:
                        closest_neighbours[node[0]][0] = diff
                    else:
                        closest_neighbours[node[0]] = [diff, new_gain, node[2]]

    return sorted(closest_neighbours.items(), key=lambda x: x[1][0], reverse=True) 

def chooseX(solutions, intersection, A, n, tour, t1, last, gain, broken, joined):
    if len(broken) >= 5: ############################################# 1
        return False, None, None
    around = []
    if len(broken) == 3:  # Rule 9 - selecting x4, larger c(x4)
        pred, succ = nodes_around(tour, last) # TODO in: path, index   out: ((node1, index1),(node2, index2))
        if A[pred, last] > A[succ, last] and check_tour(tour, broken | {make_pair(pred, last)}, joined | {make_pair(pred, t1)}):
            around = [pred]
        elif check_tour(tour, broken | {make_pair(succ, last)}, joined | {make_pair(succ, t1)}):
            around = [succ]
    else:
        around = nodes_around(tour, last) # TODO in: path, index   out: ((node1, index1),(node2, index2))

    for t2i in around:
        xi = make_pair(last, t2i)
        if len(broken) >= 2 and xi in intersection:  # Rule 6 - xi can't be broken if common link of multiple tours ############################# 3
            continue
        new_gain = gain + A[last, t2i]

        if xi not in joined and xi not in broken:
            total_gain = new_gain - A[t2i, t1]
            is_tour, new_tour = check_tour(tour, broken | {xi}, joined | {make_pair(t2i, t1)}) # Rule 3 - selecting xi, (t2i, t1) must make a valid tour

            if is_tour:
                if tuple(new_tour) in solutions:  # Rule 7 - new tour == previous tour - break 
                    return False, None, None

                if total_gain > 0:
                    return True, new_tour, path_length(new_tour, A, n)

                choice, new_tour, new_tour_cost = chooseY(solutions, intersection, A, n, tour, t1, t2i, new_gain, broken | {xi}, joined)
                return choice, new_tour, new_tour_cost # if choice: ######################################### 2

    return False, None, None

def chooseY(solutions, intersection, A, n, tour, t1, t2i, gain, broken, joined):
    closest_neighbours = closest(A, t2i, tour, gain, broken)

    for node, (_, Gi) in closest_neighbours:
        yi = make_pair(t2i, node)
        
        if not tour_contains(tour, yi):
            is_better, new_tour, new_tour_cost = chooseX(solutions, intersection, A, n, tour, t1, node, Gi, broken, joined | {yi})
            if is_better:
                return is_better, new_tour, new_tour_cost

    return False, None, None

# Steps 4, 5, 6, 7, 8, 9, 10