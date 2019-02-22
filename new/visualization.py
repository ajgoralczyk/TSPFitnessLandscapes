import igraph
from helpers import *
import numpy as np

### data visualization

def generate_projection_image(V, E, V_lon, E_lon, A, n, out_file, g_min=None):
    E_probs = get_edges_probs(V, E)
    E = set(E.keys())

    print("projection nodes in LON", len(V & V_lon), " / ", len(V) )
    print("projection edges in LON", len(E & set(E_lon.keys())), " / ", len(E))

    results = sorted([path_length(s, A, n) for s in V])  # ascending
    if not g_min:
        g_min = results[0]
    threshold = results[400]  # max number of nodes
    V = {s for s in V if path_length(s, A, n) <= threshold}  # s - path
    V_ = {s: (i, path_length(s, A, n)) for i, s in enumerate(V)}

    Not_Sinks = set()
    for s in V:  # TODO optimal?
        for (v, u) in E:
            if v == s:
                Not_Sinks.add(s)
                break

    V_c = np.zeros(len(V_), dtype=object)
    for s, (i, r) in V_.items():
        V_c[i] = (s, r)
    E_ = [(V_[s1][0], V_[s2][0]) for s1, s2 in E if s1 in V_ and s2 in V_]
    E_size = [5 * E_probs[s1, s2] for s1, s2 in E if s1 in V_ and s2 in V_]  # TODO
    pos_glob = find_pos_glob(V_, E, g_min, A, n)

    g = igraph.Graph(directed=True)
    g.add_vertices(len(V_))
    g.add_edges(E_)

    visual_style = {}
    visual_style["layout"] = \
        g.layout_fruchterman_reingold(maxiter=5000)
    visual_style["vertex_color"] = ['red' if t[0] in pos_glob and t[0] in V_lon else
                                    'pink' if t[0] in pos_glob and t[0] not in V_lon else
                                    '#87CEFA' if t[0] not in V_lon else
                                    'blue'
                                    for t in V_c]
    visual_style["vertex_frame_color"] = \
        [visual_style["vertex_color"][i] if t[0] in Not_Sinks else 'black'
         for i, t in enumerate(V_c)]
    visual_style["vertex_frame_width"] = [2 for i in V_c]
    visual_style["vertex_size"] = [10 if t[0] in Not_Sinks else 20 for t in V_c]
    visual_style["edge_color"] = ['darkgrey' if e in set(E_lon.keys()) else
                                  'lightgrey'
                                  for e in E_]
    visual_style["edge_width"] = E_size
    visual_style["bbox"] = (0, 0, 1800, 1000)

    igraph.summary(g)
    image = igraph.plot(g, **visual_style)
    image.save(out_file + '.png')
    print("image ", out_file)
    pass


def generate_image(V, E, A, n, out_file, g_min=None): # generate png image from graph file
    E_probs = get_edges_probs(V, E)
    E = set(E.keys())
    results = sorted([path_length(s, A, n) for s in V])  # ascending
    if not g_min:
        g_min= results[0]
    threshold = results[400]  # max number of nodes
    V = { s for s in V if path_length(s, A, n) <= threshold}  # s - path
    V_ = { s : (i, path_length(s, A, n)) for i, s in enumerate(V)}

    Not_Sinks = set()
    for s in V:  # TODO optimal?
        for (v, u) in E:
            if v == s:
                Not_Sinks.add(s)
                break

    V_c = np.zeros(len(V_), dtype=object)
    for s, (i, r) in V_.items():
        V_c[i] = (s, r)
    E_ = [(V_[s1][0], V_[s2][0]) for s1, s2 in E if s1 in V_ and s2 in V_]
    E_size = [5 * E_probs[s1, s2] for s1, s2 in E if s1 in V_ and s2 in V_]
    pos_glob = find_pos_glob(V_, E, g_min, A, n)

    g = igraph.Graph(directed=True)
    g.add_vertices(len(V_))
    g.add_edges(E_)

    visual_style = {}
    visual_style["layout"] = \
        g.layout_fruchterman_reingold(maxiter=5000)
    visual_style["vertex_color"] = ['red' if t[0] in pos_glob else 'blue'
                for t in V_c]
    visual_style["vertex_frame_color"] = \
        [visual_style["vertex_color"][i] if t[0] in Not_Sinks else 'black'
        for i, t in enumerate(V_c)]
    visual_style["vertex_frame_width"] = [2 for i in V_c]
    visual_style["vertex_size"] = [10 if t[0] in Not_Sinks else 20 for t in V_c]
    visual_style["edge_width"] = E_size
    visual_style["bbox"] = (0, 0, 1800, 1000)

    igraph.summary(g)
    image = igraph.plot(g, **visual_style)
    image.save(out_file + '.png')
    print("image ", out_file)


def gen_sub_images(filename, T, s): # automated subinstances graph image files generation
    for t in range(T):
        sub_file = filename + "_" + str(s) + "_" + str(t)
        generate_image(sub_file)


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


def dfs(v, V, E, g_min, prev, A, n):
    if path_length(v, A, n) == g_min:
        return True
    if v not in E:
        return False
    for u in E[v]:
        if u == prev:
            continue
        if dfs(u, V, E, g_min, v, A, n):
            return True
    return False


def find_pos_glob(V, E, g_min, A, n):
    E_ = adjacency_list(V, E)
    pos_glob = set()
    for v in V.keys():
        if dfs(v, V, E_, g_min, None, A, n):
            pos_glob.add(v)
    return pos_glob


def get_edges_probs(V, E):
    E_ = adjacency_list(V, set(E.keys()))  # key - (s1,s2)
    E_probs = {}
    for v, l in E_.items():
        s = sum([E[(v, neigh)] for neigh in l])
        for neigh in l:
            E_probs[(v, neigh)] = E[(v, neigh)] / s
    return E_probs  # probability of certain edge in all edges from certain node

