from copy import deepcopy
from helpers import *

def optimise_path(path, A, n):
    solutions = set()
    better = True

    while better:
        better, path = improve(solutions, path, A, n)
        solutions.add(path)
    return path


def improve(solutions, path, A, n):
    for t1 in path:
        around_t1 = nodes_around(path, t1)

        for t2 in around_t1:
            broken = {[make_pair(t1, t2)]}
            gain = A[t1, t2]  # initial savings
            closest_neighbours = closest(A, n, t2, path, gain, broken, set())
            tries = 5  # number of neighbours to try

            for t3, (_, Gi) in closest_neighbours:
                if t3 not in around_t1:  # make sure that the new node is none of t_1's neighbours, so it does not belong to the tour.
                    joined = {[make_pair(t2, t3)]}

                    is_better, better_path, better_path_cost = chooseX(solutions, A, n, path, t1, t3, Gi, broken, joined)  # return to Step 2, that is the initial loop
                    if is_better:
                        return True, better_path

                    tries -= 1
                    if tries == 0:  # explored enough nodes, change t_2
                        break

    return False, path


def closest(A, n, t2i, tour, gain, broken, joined):
    closest_neighbours = {}
    neighbours = list(range(n))
    neighbours.remove(t2i)

    for node in neighbours: # create the neighbours of t_2i
        yi = make_pair(t2i, node)
        new_gain = gain - A[t2i, node]

        if new_gain > 0 and yi not in broken and not tour_contains(tour, yi):
            for next_node in nodes_around(tour, node):
                xi = make_pair(node, next_node)

                if xi not in broken and xi not in joined:  # TODO verify it is enough (we check if the tour is valid in `chooseX`)
                    diff = A[node, next_node] - A[t2i, node]

                    if node in closest_neighbours and diff > closest_neighbours[node][0]:  # TODO - what's that?
                        closest_neighbours[node][0] = diff
                    else:
                        closest_neighbours[node] = [diff, new_gain]

    return sorted(closest_neighbours.items(), key=lambda x: x[1][0], reverse=True)  # sort the neighbours by potential gain


def chooseX(solutions, A, n, tour, t1, last, gain, broken, joined):
    if len(broken) == 4:  # TODO why?
        pred, succ = nodes_around(tour, last)

        if A[pred, last] > A[succ, last]:  # give priority to the longest edge for x_4
            around = [pred]
        else:
            around = [succ]
    else:
        around = nodes_around(tour, last)

    for t2i in around:
        xi = make_pair(last, t2i)
        new_gain = gain + A[last, t2i]  # gain at current iteration

        if xi not in joined and xi not in broken:  # TODO - what about original path?
            added = deepcopy(joined)
            removed = deepcopy(broken)
            removed.add(xi)

            added.add(make_pair(t2i, t1))  # try to close the tour
            total_gain = new_gain - A[t2i, t1]
            is_tour, new_tour = check_tour(tour, removed, added)

            if is_tour:  # we allow non-sequential exchange with i = 2
                if str(new_tour) in solutions:  # stop the search if we come back to the same solution
                    return False, None, None

                if total_gain > 0: # save the current solution if the tour is better
                    return True, new_tour, path_length(new_tour, A, n)

            if len(added) <= 2:
                choice, new_tour, new_tour_cost = chooseY(solutions, A, n, tour, t1, t2i, new_gain, removed, joined)  # pass on the newly "removed" edge but not the total gain
                if len(broken) == 2 and choice:
                    return True, new_tour, new_tour_cost
                else:
                    return choice, new_tour, new_tour_cost  # single iteration for i > 2

    return False, None, None


def chooseY(solutions, A, n, tour, t1, t2i, gain, broken, joined):  # return whether we found an improved tour
    ordered = closest(A, n, t2i, tour, gain, broken, joined)

    if len(broken) == 2:  # check the five nearest neighbours when i = 2
        top = 5
    else:  # otherwise the closest only
        top = 1

    for node, (_, Gi) in ordered:
        yi = make_pair(t2i, node)
        added = deepcopy(joined)
        added.add(yi)

        is_better, new_tour, new_tour_cost = chooseX(solutions, A, n, tour, t1, node, Gi, broken, added)  # stop at the first improving tour
        if is_better:
            return is_better, new_tour, new_tour_cost

        top -= 1
        if top == 0:
            return False, None, None

    return False, None, None



