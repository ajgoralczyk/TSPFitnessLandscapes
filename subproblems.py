from metrics import *
import os

def TSP_sub_problems_generation(problems_foldername, subinstances_array): # subproblems creation
    for filename in os.listdir(problems_foldername):
        if filename.endswith('.tsp'):
            A, n = parse_TSP_from_file(problems_foldername + '/' + filename)
            out_file = filename.split('.')[0]
            out_folder = problems_foldername + "/data_" + out_file
            nodes_array = list(range(n))
            save_TSP(A, n, nodes_array, out_folder + '/' + out_file)
            for amount, nodes_to_remove in subinstances_array:
                generate_subinstances(A, n, out_folder + '/' + out_file, amount, nodes_to_remove)


if __name__ == '__main__':
    TSP_sub_problems_generation("data", [(5, 2),(5, 5),(5, 10)])
