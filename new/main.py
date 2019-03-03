from fitness_landcape import *
from visualization import *
import os
import datetime

def TSP_sub_problems_generation(problems_foldername):
    for filename in os.listdir(problems_foldername):
        if filename.endswith('.tsp'):
            A, n = parse_TSP_from_file(problems_foldername + '/' + filename)
            out_file = filename.split('.')[0]
            out_folder = problems_foldername + "/data_" + out_file
            nodes_array = list(range(n))
            save_TSP(A, n, nodes_array, out_folder + '/' + out_file)
            generate_subinstances(A, n, out_folder + '/' + out_file, 5, 2)
            generate_subinstances(A, n, out_folder + '/' + out_file, 5, 5)
            generate_subinstances(A, n, out_folder + '/' + out_file, 5, 10)


def main_part2__LONs(instances_foldername, lons_foldername, metrics_foldername, K):
    for filename in os.listdir(instances_foldername):
        if filename.endswith('.tsp'):
            out_folder = filename.split('.')[0]

            for instance_filename in os.listdir(instances_foldername + "/data_" + out_folder):
                out_file = instance_filename.split('.')[0]
                print("start", datetime.datetime.now())
                A, n, nodes_array = load_TSP(instances_foldername + "/data_" + out_folder + "/" + instance_filename)

                L, E, best_path_length, best_path, successes, mean_iters = generate_LON(A, 10, 10, K)
                save_LON(L, E, A, n, nodes_array, lons_foldername + "/" + out_file + ".g")
                save_metrics((best_path_length, best_path, successes, mean_iters), metrics_foldername + "/" + out_file + ".metrics")
                save_best(instances_foldername + "/" + out_file + '.best', best_path_length, best_path)
                print("end", datetime.datetime.now())
                print("LON ", out_file)


def main_part3__images(lons_foldername, images_foldername):
    for filename in os.listdir(lons_foldername):
        L, E, A, n, nodes_array = load_LON(lons_foldername + "/" + filename)
        out_file = filename.split('.')[0]

        generate_image(L, E, A, n, images_foldername + "/" + out_file)


def main_part4__metrics(best_foldername, lons_foldername, performance_metrics_foldername, metrics_foldername):
    for filename in os.listdir(lons_foldername):
        L, E, A, n, nodes_array = load_LON(lons_foldername + "/" + filename)
        out_file = filename.split('.')[0]
        performance_metrics = load_metrics(performance_metrics_foldername + "/" + out_file + ".metrics")
        network_metrics = generate_network_metrics(L, E, A, n, performance_metrics)
        # save_best(best_foldername, best_foldername + "/" + out_file + ".metrics")
        save_metrics(network_metrics, metrics_foldername + "/" + out_file + ".metrics")


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


# TSP_sub_problems_generation("data")

if __name__ == '__main__':
    main_part2__LONs("data", "checking2/1_lons", "checking2/3_performance_metrics", 1)












