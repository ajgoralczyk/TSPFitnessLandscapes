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

    def select_next(self, possible_paths, _):
        self.select_next = self.select_next_post
        return possible_paths[0]

    def select_next_post(self, possible_paths, new_tour):
        if len(new_tour) == self.length and (possible_paths[0][0] == new_tour[0] or possible_paths[1][0] == new_tour[0]):
            return []
        if possible_paths[0][0] == new_tour[-2]:
            return possible_paths[1]
        else:
            return possible_paths[0]

    def create_path_fragments(self):
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
                self.adjacent[v1] = [[v2]]

    def generate_tour(self):
        self.create_path_fragments()

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
                    return True, new_tour
                else:
                    return False, None