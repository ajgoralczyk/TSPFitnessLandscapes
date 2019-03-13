class TourCheck():
    def __init__(self, tour, broken, broken_indexes, joined):
        self.tour = tour
        self.length = len(tour)
        self.broken = broken
        self.broken_indexes = sorted(broken_indexes)
        self.joined = joined
        self.adjacent = {}

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

    def add_to_adjacent(self, last_unbroken, index):
        if last_unbroken < index - 1:
            self.adjacent[self.tour[last_unbroken]] = [self.tour[last_unbroken + 1:index]]
            self.adjacent[self.tour[index - 1]] = [list(reversed(self.tour[last_unbroken:index - 1]))]

    def generate_tour(self):
        last_unbroken = -1
        for index in self.broken_indexes:
            self.add_to_adjacent(last_unbroken, index + 1)
            last_unbroken = index + 1
        self.add_to_adjacent(last_unbroken, self.length)

        for v1, v2 in self.joined:
            try:
                self.adjacent[v1].append([v2])
            except KeyError:
                self.adjacent[v1] = [[v2]]

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