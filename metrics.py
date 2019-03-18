import math
from visualization import *
from in_out import *


### metrics
def generate_metrics(V, E, A, n, performance_metrics, best_path_length, best_path, chained_lk_runs):
    perf_best_path_length, perf_best_path, successes, mean_iters, L_in_degree = performance_metrics
    nodes_sum = len(V) # number of nodes in LON
    edges_sum = len(E.items())  # number of nodes in LON

    if best_path_length is not None and perf_best_path_length > best_path_length:
        success_rate = 0.0
    else:
        success_rate = successes/chained_lk_runs

    x = min(L_in_degree.values())

    V_ = V.copy()
    for (v1, _) in E.keys():
        if v1 in V_:
             V_.remove(v1)
    sinks = len(V_) # number of sinks in LON

    outgoing = adjacency_list(E)
    E_ = {} # edge weights
    L_out_degree = {}
    for v in outgoing.keys():
        edges = 0
        for v_ in outgoing[v]:
            edges += E[(v, v_)]
        L_out_degree[v] = edges
        for v_ in outgoing[v]:
            E_[(v, v_)] = E[(v, v_)]/L_in_degree[v]

    # for node in V:
    #     if node not in L_out_degree.keys():
    #         print('in', L_in_degree[node], 'out 0')
    #     elif L_in_degree[node] != L_out_degree[node]:
    #         print('in', L_in_degree[node], 'out', L_out_degree[node])

    incoming = adjacency_list(E, True)
    in_strengths = {}
    for v in V_: # foreach sink - weighted incoming degree
        strength = 0
        for v_ in incoming[v]:
            strength += E_[(v_, v)]
        in_strengths[v] = (path_length(v, A, n), strength)

    optimal_length = math.inf
    optimal_strength = 0
    total_strength = 0
    optimal_sinks = set()
    for v, (length, strength) in in_strengths.items():
        if length < optimal_length:
            optimal_length = length
            optimal_strength = strength
            total_strength += strength
            optimal_sinks = {v}
        elif length == optimal_length:
            optimal_strength += strength
            total_strength += strength
            optimal_sinks.add(v)
        else:
            total_strength += strength
    relative_in_strength = optimal_strength/total_strength  # relative in-strength of the globally optimal sink

    S_ = optimal_sinks
    incoming_ = incoming.copy()
    while True:
        S = S_.copy()
        for v in S:
            if v in incoming_.keys():
                for v_ in incoming_[v]:
                    S_.add(v_)
                incoming_.pop(v)
        if len(S) == len(S_):
            break
    nodes_in_optimal_funnels = len(S_)/nodes_sum # proportion of nodes in the globally optimal funnels

    fitnesses = set()
    for v in V:
        fitnesses.add(path_length(v, A, n))
    nodes_with_unique_path_length = len(fitnesses)/nodes_sum # proportion of nodes with unique fitness value (path length)

    return tuple([nodes_sum, edges_sum, success_rate, mean_iters, sinks, relative_in_strength, nodes_in_optimal_funnels, nodes_with_unique_path_length])


### LON projection !
def project_LON(V, E, A_, n_, nodes_array):  # TODO check
    V_ = set()
    E_1 = {}
    E_2 = {}  # without loops, without upstream edges
    E_3 = {}  # without loops, with reversed upstream edges
    loops = 0
    upstream_edges = 0
    for v in V:
        v_ = tuple([np.where(nodes_array == node)[0][0] for node in v if node in nodes_array])
        if v_ not in V_:
            V_.add(v_)

    for (v1, v2) in E.keys():
        v1_ = tuple([np.where(nodes_array == node)[0][0] for node in v1 if node in nodes_array])
        v2_ = tuple([np.where(nodes_array == node)[0][0] for node in v2 if node in nodes_array])
        if (v1_, v2_) in E_1:
            E_1[(v1_, v2_)] += E[(v1, v2)]
        else:
            E_1[(v1_, v2_)] = E[(v1, v2)]

    for (v1, v2) in E_1.keys():  # E_2 without upstream_edges
        if v1 == v2:  # loop
            loops += 1
        elif path_length(v2, A_, n_) > path_length(v1, A_, n_):
            upstream_edges += 1
            E_3[(v2, v1)] = E_1[(v1, v2)]
        else:
            E_2[(v1, v2)] = E_1[(v1, v2)]
            E_3[(v1, v2)] = E_1[(v1, v2)]

    print('loops', loops, 'upstream edges', upstream_edges)
    return V_, E_1, E_2, E_3, loops, upstream_edges


def generate_projection_metrics(L, E, A, n, foldername):
    pass

### sub-problems generation
def generate_subinstances(A, n, out_file, amount, nodes_removed):
    for t in range(amount):
        A_, n_, nodes_array = random_subinstance(A, n, n-nodes_removed)
        sub_name = out_file + "_" + str(nodes_removed) + "_" + str(t)
        save_TSP(A_, n_, nodes_array, sub_name)


def random_subinstance(A, n, n_):
    picked_v = np.sort(np.random.choice(range(n), n_, replace=False))
    return A[np.array(picked_v)[:,None], np.array(picked_v)], n_, picked_v  # only selected rows & columns




