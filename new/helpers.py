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


class TourCheck():

    def __init__(self, tour, broken, joined):
        self.tour = tour
        self.length = len(tour)
        self.broken = broken
        self.joined = joined
        self.adjacent = {}
        self.path_fragments = {}
        # self.path_disjoint = []

    def add_to_adjacent(self, last_unbroken, index):
        if last_unbroken != index - 1:
            if self.tour[last_unbroken] in self.adjacent:
                self.adjacent[self.tour[last_unbroken]].append(self.tour[last_unbroken + 1:index])
            else:
                self.adjacent[self.tour[last_unbroken]] = [self.tour[last_unbroken + 1:index]]

            if self.tour[index - 1] in self.adjacent:
                self.adjacent[self.tour[index - 1]].append(list(reversed(self.tour[last_unbroken:index - 1])))
            else:
                self.adjacent[self.tour[index - 1]] = [list(reversed(self.tour[last_unbroken:index - 1]))]

    def add_fragment(self, node1, node2, indexes):
        try:
            self.path_fragments[node1].add((node2, indexes))
        except KeyError:
            self.path_fragments[node1] = {(node2, indexes)}
        try:
            self.path_fragments[node2].add((node1, indexes))
        except KeyError:
            self.path_fragments[node2] = {(node1, indexes)}

    def select_next(self, possible_paths, _):
        self.select_next = self.select_next_post
        return min(possible_paths, key=lambda list: list[0])

    def select_next_post(self, possible_paths, new_tour): # TODO: check
        if len(new_tour) == self.length and (possible_paths[0][0] == new_tour[0] or possible_paths[1][0] == new_tour[0]):
            return []
        if possible_paths[0][0] == new_tour[-2]:
            return possible_paths[1]
        else:
            return possible_paths[0]

    def check_tour(self):
        if (self.tour[-1], self.tour[0]) not in self.broken:
            self.path_fragments[self.tour[-1]] = {(self.tour[0], (0,0))} # neighbour node + indexes of nodes in between
            self.path_fragments[self.tour[0]] = {(self.tour[-1], (0,0))}
        last_unbroken = 0
        for index in range(self.length):
            if (self.tour[index-1], self.tour[index]) in self.broken:
                if last_unbroken != index - 1:
                    self.add_fragment(self.tour[index-1], self.tour[last_unbroken], (last_unbroken+1, index-1))
                last_unbroken = index
        if last_unbroken != self.length-1:
            self.add_fragment(self.tour[self.length-1], self.tour[last_unbroken], (last_unbroken+1, self.length-1))

        for v1, v2 in self.joined:
            self.add_fragment(v1, v2, (0,0))

        node = self.tour[0]
        previous = None
        new_tour = [self.tour[0]]
        length = len(self.path_fragments)

        while True:
            try:
                possible_paths = self.path_fragments[node]
                if len(possible_paths) != 2:
                    return False
                link1, link2, *_ = possible_paths
                if link1[0] == previous:
                    next = link2
                else:
                    next = link1
                # new_tour.extend(next)
                length -= 1
                del self.path_fragments[node]
                previous = node
                node = next[0]
            except KeyError:
                if length == 0 and node == new_tour[0]: #### TODO
                    return True
                else:
                    return False


    def join_tour(self):
        pass

    def generate_tour(self):
        if (self.tour[-1], self.tour[0]) not in self.broken:
            self.adjacent[self.tour[-1]] = [[self.tour[0]]]
            self.adjacent[self.tour[0]] = [[self.tour[-1]]]
        last_unbroken = 0
        for index in range(1,self.length):
            if (self.tour[index-1], self.tour[index]) in self.broken:
                self.add_to_adjacent(last_unbroken, index)
                last_unbroken = index
        self.add_to_adjacent(last_unbroken, self.length)

        for v1, v2 in self.joined:
            try:
                self.adjacent[v1].append([v2])
            except KeyError:
                return False, None

        node = self.tour[0]
        new_tour = [self.tour[0]]

        while True:
            try:
                possible_paths = self.adjacent[node]
                if len(possible_paths) != 2:
                    return False, None
                next = self.select_next(possible_paths, new_tour)
                new_tour.extend(next)
                del self.adjacent[node]
                node = new_tour[-1]
            except KeyError:
                if len(new_tour) == self.length:
                    return len(new_tour) == self.length, new_tour
                else:
                    return False, None