from metrics import *
from visualization import *
import os
# import datetime
# import sys


def LON_visualization(best_foldername, lons_foldername, images_foldername):
    for filename in os.listdir(lons_foldername):
        L, E, A, n, nodes_array = load_LON(lons_foldername + "/" + filename)
        out_file = filename.split('.')[0]
        best_path_length, best_path = load_best(best_foldername + "/" + out_file + ".best")
        generate_image(L, E, A, n, images_foldername + "/" + out_file, best_path_length)


def metrics(best_foldername, lons_foldername, performance_metrics_foldername, metrics_foldername, chained_lk_runs):
    for filename in os.listdir(lons_foldername):
        L, E, A, n, nodes_array = load_LON(lons_foldername + "/" + filename)
        out_file = filename.split('.')[0]
        performance_metrics = load_metrics(performance_metrics_foldername + "/" + out_file + ".metrics")
        best_path_length, best_path = load_best(best_foldername + "/" + out_file + ".best")
        metrics = generate_metrics(L, E, A, n, performance_metrics, best_path_length, best_path, chained_lk_runs)

        save_metrics(metrics, metrics_foldername + "/" + out_file + ".metrics")


def main_part5__projections(lons_foldername, projections_foldername):
    for filename in os.listdir(lons_foldername):
        out_file = filename.split('.')[0]
        is_main = len(out_file.split('_')) == 1

        if is_main:
            L_main, E_main, A_main, n_main, nodes_array_main = load_LON(lons_foldername + "/" + filename)
        else:
            L, E, A, n, nodes_array = load_LON(lons_foldername + "/" + filename)
            L_, E_1, E_2, E_3, loops, upstream_edges = project_LON(L_main, E_main, A, n, nodes_array)
            save_LON(L_, E_3, A, n, nodes_array, projections_foldername + "/" + out_file + ".g")


def main_part6__projection_images(projections_foldername, lons_foldername, images_foldername, projection_images_foldername):
    for filename in os.listdir(projections_foldername):
        L, E, A, n, nodes_array = load_LON(projections_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        L_, E_, A_, n_, nodes_array_ = load_LON(lons_foldername + "/" + filename)

        results1 = sorted([path_length(s, A, n) for s in L])  # ascending
        results2 = sorted([path_length(s, A_, n_) for s in L_])  # ascending
        g_min = min(results1[0], results2[0])

        generate_image(L_, E_, A_, n_, images_foldername + "/" + out_file, g_min)
        generate_projection_image(L, E, L_, E_, A, n, projection_images_foldername + "/" + out_file, g_min)


def main_part7__projection_metrics(projections_foldername, projection_metrics_foldername):
    for filename in os.listdir(projections_foldername):
        L, E, A, n, nodes_array = load_LON(projections_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        generate_projection_metrics(L, E, A, n, projection_metrics_foldername + "/" + out_file)

if __name__ == '__main__':
    metrics("checking_data", "checking/1_lons", "checking/3_performance_metrics", "checking/4_network_metrics", 1000)
    # metrics("data/data_bays29", "new_results/1_lons", "new_results/3_performance_metrics", "new_results/4_network_metrics", 1000)