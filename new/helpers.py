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


def path_length(p, A, n):
    s = 0.0
    for i in range(n):  # [0..n-1]
        s += A[p[i-1], p[i]]  # p[-1] - last element
    return s

