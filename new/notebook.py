from IPython.display import HTML, display
import os
import in_out as io

def print_images(images_foldername):
    strings = []
    for filename in os.listdir(images_foldername):
        strings.append("<div style='width: 30%; margin: 1.5%; float: left'>"
                       "<img src='" + images_foldername + "/" + filename + "' /><span>" + filename + "</span></div>")
    imagesHTML = ''.join(strings)
    display(HTML(imagesHTML))


def print_images_and_projections(images_foldername, projections_foldername):
    strings = []
    for filename in os.listdir(images_foldername):
        strings.append("<div style='width: 45%; margin: 2.5%; float: left'>"
                       "<img src='" + projections_foldername + "/" + filename + "' /><span>" + filename + " - projection</span></div>")
        strings.append("<div style='width: 45%; margin: 2.5%; float: left'>"
                       "<img src='" + images_foldername + "/" + filename + "' /><span>" + filename + " - LON</span></div>")

    imagesHTML = ''.join(strings)
    display(HTML(imagesHTML))


def print_metrics(performance_metrics_foldername, network_metrics_foldername):
    success_rate = []  # success rate
    iters_to_success = []  # mean number of iterations to success
    nodes = []  # number of nodes in LON
    edges = []
    sinks = []  # number of sinks in LON
    relative_in_strength = []  # relative in-strength of the globally optimal sink
    nodes_in_optimal_funnels = []  # proportion of nodes in the globally optimal funnels
    nodes_with_unique_path_length = []  # proportion of nodes with unique path length
    for filename in os.listdir(performance_metrics_foldername):
        performance_metrics = io.load_metrics(performance_metrics_foldername + "/" + filename)
            # best_path_length, best_path, successes, mean_iters
        network_metrics = io.load_metrics(network_metrics_foldername + "/" + filename)
            # nodes, edges, sinks, in_strength, nodes_in_optimal_funnels, nodes_with_unique_path_length
        success_rate.append(performance_metrics[2]/1000)  ##############################################################
        iters_to_success.append(format(performance_metrics[3], '.2f'))
        nodes.append(network_metrics[0])
        edges.append(network_metrics[1])
        sinks.append(network_metrics[2])
        relative_in_strength.append(format(network_metrics[3], '.2f'))
        nodes_in_optimal_funnels.append(format(network_metrics[4], '.2f'))
        nodes_with_unique_path_length.append(format(network_metrics[4], '.2f'))

    print("Success rate", success_rate)
    print("Iterations to success", iters_to_success)
    print("Number of nodes", nodes)
    print("Number of edges", edges)
    print("Number of sinks", sinks)
    print("Relative in-strength", relative_in_strength)
    print("Proportion of nodes in optimal funnels", nodes_in_optimal_funnels)
    print("Proportion of nodes with unique path length", nodes_with_unique_path_length)
