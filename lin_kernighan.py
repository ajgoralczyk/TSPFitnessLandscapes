from helpers import *
from tour_check import *
from itertools import starmap

class LK:
    def __init__(self, A, n, closest_nodes):
        self.A = A
        self.n = n
        self.closest_nodes = closest_nodes

    def closest_tuples(self):
        def closest_tuple(node1, node2):
            return (node2, self.indexes[node2], self.A[node1, node2])

        closest = {}
        self.indexes = {}
        for i in range(self.n):
            self.indexes[self.tour[i]] = i
        for i in range(self.n):
            closest[i] = list(starmap(closest_tuple, [(i, node) for node in self.closest_nodes[i]]))
        return closest

    def optimize_path(self, tour): # Step 1
        self.tour = tour
        self.edges = set()
        for i in range(self.n):
            self.edges.add((self.tour[i - 1], self.tour[i]))
            self.edges.add((self.tour[i], self.tour[i - 1]))

        solutions = set()
        intersection = set()
        previous_edges = set()
        better = True
        i = 1

        while better:
            closest_tuples = self.closest_tuples() # (node, index, cost)
            better, better_path, better_path_length = self.improve(solutions, intersection, closest_tuples)
            solutions.add(normalize_path(better_path))

            if len(previous_edges) == 0:
                for index in range(len(better_path)):
                    previous_edges.add((better_path[index - 1], better_path[index]))
                    previous_edges.add((better_path[index], better_path[index - 1]))
            elif len(intersection) == 0:
                edges = set()
                for index in range(len(better_path)):
                    edges.add((better_path[index - 1], better_path[index]))
                    edges.add((better_path[index], better_path[index - 1]))
                intersection = previous_edges & edges
            else:
                edges = set()
                for index in range(len(better_path)):
                    edges.add((better_path[index - 1], better_path[index]))
                    edges.add((better_path[index], better_path[index - 1]))
                intersection = intersection & edges

            self.tour = better_path
            i += 1

        return self.tour

    def improve(self, solutions, intersection, closest_tuples):
        for index_t1, t1 in enumerate(self.tour):  # Step 2, 12
            around_t1 = nodes_around(self.tour, index_t1)

            for t2, index_t2 in around_t1:  # Step 3, 11
                broken = {(t1, t2), (t2, t1)}
                broken_indexes = [min(index_t1, index_t2)]
                gain = self.A[t1, t2]
                closest_neighbours = self.closest(t2, gain, broken, closest_tuples[t2])

                for t3, (_, Gi, index_t3) in closest_neighbours:
                    joined = {(t3, t2), (t2, t3)}  # Rule 1 - only sequential exchanges

                    is_better, better_path, better_path_cost = self.chooseX(solutions, intersection, closest_tuples, t1, index_t1, t3, index_t3, Gi, broken, broken_indexes, joined, 2)
                    if is_better:
                        return is_better, better_path, better_path_cost

        return False, self.tour, None  # Step 13

    def closest(self, t2i, gain, broken, closest_tuples): # Rule 5 - 5 closest neighbours
        neighbours = {}
        for node, node_index, yi_length in closest_tuples: # (node, index, edge_distance)
            yi = (t2i, node)
            new_gain = gain - yi_length  # Rule 2 - selecting yi, that Gi (g1 + g2 + ... + gi) > 0

            if new_gain > 0 and yi not in broken and yi not in self.edges:  # Rule 4 - X, Y separate
                for next_node, index_next_node in nodes_around(self.tour, node_index):
                    xi = (node, next_node)

                    if xi not in broken:
                        diff = self.A[node, next_node] - yi_length # Rule 8 - selecting yi with priority c(xi+1) - c(yi)

                        if node in neighbours and diff > neighbours[node][0]:
                            neighbours[node][0] = diff
                        else:
                            neighbours[node] = [diff, new_gain, node_index]

        return sorted(neighbours.items(), key=lambda x: x[1][0], reverse=True)

    def chooseX(self, solutions, intersection, closest_tuples, t1, index_t1, last, index_last, gain, broken, broken_indexes, joined, depth):
        # if len(broken) >= 9: ##################################################### 1
        #     return False, None, None
        around = []
        new_tour = None
        if depth == 4:  # Rule 9 - selecting x4, larger c(x4)
            (pred, index_pred), (succ, index_succ) = nodes_around(self.tour, index_last)

            tc1 = TourCheck(self.tour, broken | {(pred, last), (last, pred)}, broken_indexes + [min(index_last, index_pred)], joined | {(t1, pred), (pred, t1)})
            is_tour, new_tour = tc1.generate_tour()
            if pred != t1 and self.A[pred, last] > self.A[succ, last] and is_tour:
                around = [(pred, index_pred)]
            else:
                tc2 = TourCheck(self.tour, broken | {(succ, last), (last, succ)}, broken_indexes + [min(index_last, index_succ)], joined | {(t1, succ), (succ, t1)})
                is_tour, new_tour = tc2.generate_tour()
                if succ != t1 and is_tour:
                    around = [(succ, index_succ)]
        else:
            around = nodes_around(self.tour, index_last)

        for t2i, index_t2i in around:
            xi = (last, t2i)
            if depth >= 4 and xi in intersection:  # Rule 6 - xi can't be broken if common link of multiple tours
                continue
            new_gain = gain + self.A[last, t2i]

            if xi not in joined and xi not in broken and t2i != t1:
                total_gain = new_gain - self.A[t2i, t1]

                if new_tour is None:
                    tc = TourCheck(self.tour, broken | {(last, t2i),(t2i, last)}, broken_indexes + [min(index_t2i, index_last)], joined | {(t1, t2i), (t2i, t1)})
                    is_tour, new_tour = tc.generate_tour() # Rule 3 - selecting xi, (t2i, t1) must make a valid tour
                else:
                    is_tour = True

                if is_tour:
                    if normalize_path(new_tour) in solutions:  # Rule 7 - new tour == previous tour - break
                        return False, None, None

                    if total_gain > 0:
                        return True, new_tour, path_length(new_tour, self.A, self.n)

                    choice, new_tour, new_tour_cost = self.chooseY(solutions, intersection, closest_tuples, t1, index_t1, t2i, new_gain, broken | {(last, t2i),(t2i, last)}, broken_indexes + [min(index_t2i, index_last)], joined, depth)
                    if depth == 2 and not choice:
                        pass
                    else:
                        return choice, new_tour, new_tour_cost

        return False, None, None

    def chooseY(self, solutions, intersection, closest_tuples, t1, index_t1, t2i, gain, broken, broken_indexes, joined, depth):
        closest_neighbours = self.closest(t2i, gain, broken, closest_tuples[t2i])
        for node, (_, Gi, index_node) in closest_neighbours:
            is_better, new_tour, new_tour_cost = self.chooseX(solutions, intersection, closest_tuples, t1, index_t1, node, index_node, Gi, broken, broken_indexes, joined | {(t2i, node), (node, t2i)}, depth+1)
            if depth == 2 and not is_better:
                pass
            else:
                return is_better, new_tour, new_tour_cost

        return False, None, None

# Steps 4, 5, 6, 7, 8, 9, 10