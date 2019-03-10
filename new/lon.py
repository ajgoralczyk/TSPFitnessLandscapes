from in_out import *
import os
# import sys
# from multiprocessing import Pool
import time
import math
from lin_kernighan import *
from itertools import starmap

def closest_nodes(A, n):
    closest = {}
    for i in range(n):
        nodes = list(range(n))
        sorted_nodes = sorted(nodes, key=lambda n: A[i,n])
        closest[i] = sorted_nodes[1:6]
    return closest

def generate_LON(A, n, runs_amount, termination_criterion, kick_strength):  # LON sampling (Algorithm 1 from paper [1])
    T = runs_amount  # number of Chained-LK runs
    I = termination_criterion  # termination criterion of run
    L = set()  # set of local optima
    E = {}  # escape edges
    L_in_degree = {}
    closest = closest_nodes(A, n)

    run_result = {}
    iters = {}
    best_path = None
    best_path_length = math.inf

    # pool = Pool()  # for parallel operations
    begin = time.time()
    for s_res, s, iters_, L_, E_ in starmap(CLK, [(I, A, n, kick_strength, closest) for t in range(T)]):
        L = L | L_
        for k, v in E_.items():
            if k in E:
                E[k] += v
            else:
                E[k] = v

        for optimum in L_:
            if optimum in L_in_degree.keys():
                L_in_degree[optimum] += 1
            else:
                L_in_degree[optimum] = 1

        if s_res in run_result:
            run_result[s_res] += 1
            iters[s_res] += iters_
        else:
            run_result[s_res] = 1
            iters[s_res] = iters_

        if s_res < best_path_length:
            best_path_length = s_res
            best_path = s

    print("time", (time.time() - begin))
    return L, E, best_path_length, best_path, run_result[best_path_length], iters[best_path_length]/run_result[best_path_length], L_in_degree


def CLK(I, A, n, K, closest_nodes):  # Iterated local search Chained-LK
    # intensification stage: Lin-Kernighan local search
    # diversification stage: double bridge (4-exchange perturbation)

    def hashable_path(path):
        index = np.where(path == 0)[0][0]
        path_ = list(np.roll(path, -index))
        if path_[1] > path_[-1]:
            path_[1: len(path_)] = reversed(path_[1: len(path_)])
        return tuple(path_)

    lk = LK(A, n, closest_nodes)
    s = np.array(lk.optimize_path(np.random.permutation(n).tolist()))    # random path turned into local optimum
    s_res = path_length(s, A, n)  # path length for order s
    local_optimum = hashable_path(s)
    L = {local_optimum}  # set of local optima (estimation generated by sampling)
    E = {}  # escape edges (obtained by double bridge and LK)
    i = 0
    total_iters = 0
    while i < I:
        p = perturbate(s, K)  # K double-bridge operations
        p = np.array(lk.optimize_path(p.tolist()))
        p_res = path_length(p, A, n)
        i += 1
        if p_res < s_res:  # difference from article [1]
            new_local_optimum = hashable_path(p)
            L.add(new_local_optimum)
            e = (local_optimum, new_local_optimum)
            local_optimum = new_local_optimum
            if e in E:
                E[e] += 1
            else:
                E[e] = 1
            s = p
            s_res = p_res
            total_iters += i
            i = 0
    return s_res, s, total_iters, L, E


def perturbate(nodes_order, K):  # K - kick strength (how many double-bridge operations are applied)
    def double_bridge(path):
        s = np.sort(np.random.choice(path.size, 3, replace=False))  # numpy.random.choice(int, sampleSize, copies?)
        return np.hstack([path[:s[0]], path[s[2]:], path[s[1]:s[2]], path[s[0]:s[1]]])

    nodes_order_ = nodes_order.copy()
    for i in range(K):
        nodes_order_ = double_bridge(nodes_order_)
    return nodes_order_


def LONs_generation(instances_foldername, lons_foldername, metrics_foldername, K, termination_criterion):
    for filename in os.listdir(instances_foldername):
        out_file = filename.split('.')[0]
        A, n, nodes_array = load_TSP(instances_foldername + "/" + filename)
        L, E, best_path_length, best_path, successes, mean_iters, L_in_degree = generate_LON(A, n, 10, termination_criterion, K)
        save_LON(L, E, A, n, nodes_array, lons_foldername + "/" + out_file + ".g")
        save_metrics((best_path_length, best_path, successes, mean_iters, L_in_degree), metrics_foldername + "/" + out_file + ".metrics")
        save_best(instances_foldername + "_best/" + out_file + '.best', best_path_length, best_path)


if __name__ == '__main__':
    # LONs_generation(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    LONs_generation("data_check", "check/1_lons", "check/3_performance_metrics", 1, 100)