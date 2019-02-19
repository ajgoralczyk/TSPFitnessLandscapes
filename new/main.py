from fitness_landcape import *
from visualization import *
import os
import datetime

def main_part1__TSP_problems(tsp_filename, instances_foldername):  # step 1  # input bays29.tsp
    A, n = io.parse_TSP_from_file(tsp_filename)
    out_file = tsp_filename.split('.')[0]
    nodes_array = list(range(n))
    io.save_TSP(A, n, nodes_array, instances_foldername + "/" + out_file)  # nodes list, sub-instances have arrays
    generate_subinstances(A, n, instances_foldername + "/" + out_file, 9, 1)
    generate_subinstances(A, n, instances_foldername + "/" + out_file, 9, 2)
    generate_subinstances(A, n, instances_foldername + "/" + out_file, 10, 5)


def main_part2__LONs(instances_foldername, lons_foldername, metrics_foldername, K):
    for filename in os.listdir(instances_foldername):
        print("start", datetime.datetime.now())
        A, n, nodes_array = io.load_TSP(instances_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        L, E, best_path_length, best_path, successes, mean_iters = generate_LON(A, 1000, 10000, K)
        io.save_LON(L, E, A, n, nodes_array, lons_foldername + "/" + out_file + ".g")
        io.save_metrics((best_path_length, best_path, successes, mean_iters), metrics_foldername + "/" + out_file + ".metrics")
        print("end", datetime.datetime.now())
        print("LON ", out_file)


def main_part3__images(lons_foldername, images_foldername):
    for filename in os.listdir(lons_foldername):
        L, E, A, n, nodes_array = io.load_LON(lons_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        generate_image(L, E, A, n, images_foldername + "/" + out_file)


def main_part4__metrics(lons_foldername, performance_metrics_foldername, metrics_foldername):
    for filename in os.listdir(lons_foldername):
        L, E, A, n, nodes_array = io.load_LON(lons_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        performance_metrics = io.load_metrics(performance_metrics_foldername + "/" + out_file + ".metrics")
        network_metrics = generate_network_metrics(L, E, A, n, performance_metrics)
        io.save_metrics(network_metrics, metrics_foldername + "/" + out_file + ".metrics")


def main_part5__projections(lons_foldername, projections_foldername):
    for filename in os.listdir(lons_foldername):
        out_file = filename.split('.')[0]
        is_main = len(out_file.split('_')) == 1

        if is_main:
            L_main, E_main, A_main, n_main, nodes_array_main = io.load_LON(lons_foldername + "/" + filename)
        else:
            L, E, A, n, nodes_array = io.load_LON(lons_foldername + "/" + filename)
            L_, E_1, E_2, loops, upstream_edges = project_LON(L_main, E_main, A, n, nodes_array)
            io.save_LON(L_, E_2, A, n, nodes_array, projections_foldername + "/" + out_file + ".g")


def main_part6__projection_images(projections_foldername, lons_foldername, images_foldername, projection_images_foldername):
    for filename in os.listdir(projections_foldername):
        L, E, A, n, nodes_array = io.load_LON(projections_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        L_, E_, A_, n_, nodes_array_ = io.load_LON(lons_foldername + "/" + filename)

        results1 = sorted([path_length(s, A, n) for s in L])  # ascending
        results2 = sorted([path_length(s, A_, n_) for s in L_])  # ascending
        g_min = min(results1[0], results2[0])

        generate_image(L_, E_, A_, n_, images_foldername + "/" + out_file, g_min)
        generate_image(L, E, A, n, projection_images_foldername + "/" + out_file, g_min)

def main_part7__projection_metrics(projections_foldername, projection_metrics_foldername):
    for filename in os.listdir(projections_foldername):
        L, E, A, n, nodes_array = io.load_LON(projections_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        generate_projection_metrics(L, E, A, n, projection_metrics_foldername + "/" + out_file)


# main_part1__TSP_problems("bays29.tsp", "data_bays29")
# main_part2__LONs("data_bays29", "1_bays29_1000/1_lons", "1_bays29_1000/3_performance_metrics", 1)
# main_part3__LON_images("1_bays29_1000/1_lons", "1_bays29_1000/2_images")
# main_part4__metrics("1_bays29_1000/1_lons", "1_bays29_1000/4_network_metrics")
# main_part5__projections("1_bays29_1000/1_lons", "1_bays29_1000/5_projections",
#   "1_bays29_1000/6_projection_images")
# main_part6 ...

# print(datetime.datetime.now())
# main_part2__LONs("data_bays29", "2_bays29_10000/1_lons", "2_bays29_10000/3_performance_metrics", 1)
