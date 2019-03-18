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


def print_metrics(metrics_foldername):
    # nodes_sum, edges_sum, success_rate, mean_iters, sinks, relative_in_strength, nodes_in_optimal_funnels, nodes_with_unique_path_length
    success_rate = []  # success rate
    iters_to_success = []  # mean number of iterations to success
    nodes = []  # number of nodes in LON
    edges = []
    sinks = []  # number of sinks in LON
    relative_in_strength = []  # relative in-strength of the globally optimal sink
    nodes_in_optimal_funnels = []  # proportion of nodes in the globally optimal funnels
    nodes_with_unique_path_length = []  # proportion of nodes with unique path length
    for filename in os.listdir(metrics_foldername):
        metrics = io.load_metrics(metrics_foldername + "/" + filename)
        # nodes_sum, edges_sum, success_rate, mean_iters, sinks, relative_in_strength, nodes_in_optimal_funnels, nodes_with_unique_path_length

        success_rate.append(metrics[2])
        iters_to_success.append(format(metrics[3], '.2f'))
        nodes.append(metrics[0])
        edges.append(metrics[1])
        sinks.append(metrics[4])
        relative_in_strength.append(format(metrics[5], '.2f'))
        nodes_in_optimal_funnels.append(format(metrics[6], '.2f'))
        nodes_with_unique_path_length.append(format(metrics[7], '.2f'))

    print("Success rate", success_rate)
    print("Iterations to success", iters_to_success)
    print("Number of nodes", nodes)
    print("Number of edges", edges)
    print("Number of sinks", sinks)
    print("Relative in-strength", relative_in_strength)
    print("Proportion of nodes in optimal funnels", nodes_in_optimal_funnels)
    print("Proportion of nodes with unique path length", nodes_with_unique_path_length)
