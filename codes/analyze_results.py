import ast
import matplotlib.pyplot as plt
import matplotlib.ticker
import os
import re
import statistics
import sys


def accuracy(path1, path2):
    count = 0
    for item1 in path1:
        if item1 in path2:
            count += 1

    return count/len(path1)*100


def generate_accuracy_dict(paths_dict):
    accuracy_dict = {}
    for key, value in paths_dict.items():
        if key[2] == 1:
            accuracy_dict[key] = 100
            continue
        accuracy_dict[key] = accuracy(paths_dict[(key[0], key[1], 1)], value)
    return accuracy_dict


def extract_info(regex_str, line):
    regex_str = r'.*' + regex_str + '.*'
    info_regex = re.compile(regex_str)
    info_val = None
    if info_regex.search(line):
        info_val = line.split(':')[1].strip()

    return info_val


def main():
    results_file_path = sys.argv[1]
    results_file = open(results_file_path, 'r')
    line = results_file.readline()
    paths_dict = {}
    load_time_dict = {}
    exec_time_dict = {}

    current_clustering = None
    current_num_cluster = None
    current_iteration = None
    current_data_load_time = None
    current_path_list = None
    while line:
        clustering = extract_info("clustering:", line)
        if clustering:
            current_clustering = clustering

        num_cluster = extract_info("num_cluster:", line)
        if num_cluster:
            current_num_cluster = int(num_cluster)

        iteration = extract_info("iteration:", line)
        if iteration:
            current_iteration = int(iteration)

        data_load_time = extract_info("load:", line)
        if data_load_time:
            current_data_load_time = float(data_load_time)

        path = extract_info("path:", line)
        if path:
            current_path_list = ast.literal_eval(path)

        execution_time = extract_info("exec:", line)
        if execution_time:
            current_exec_time = float(execution_time)

            current_key = (current_clustering, current_iteration, current_num_cluster)
            paths_dict[current_key] = current_path_list
            load_time_dict[current_key] = current_data_load_time
            exec_time_dict[current_key] = current_exec_time

        line = results_file.readline()

    accuracy_dict = generate_accuracy_dict(paths_dict)

    mean_accuracy_dict = {}
    mean_load_time_dict = {}
    mean_exec_time_dict = {}

    stddev_accuracy_dict = {}
    stddev_load_time_dict = {}
    stddev_exec_time_dict = {}

    clustering_list = ['kmeans', 'agglomerative']
    num_cluster_list = [1, 2, 4, 8]
    iteration_list = range(10)
    for clustering in clustering_list:
        for num_cluster in num_cluster_list:
            key = (clustering, num_cluster)
            accuracy_list = []
            load_time_list = []
            exec_time_list = []
            for iteration in iteration_list:
                orig_key = (clustering, iteration, num_cluster)
                if orig_key in accuracy_dict:
                    accuracy_list.append(accuracy_dict[orig_key])
                if orig_key in load_time_dict:
                    load_time_list.append(load_time_dict[orig_key])
                if orig_key in exec_time_dict:
                    exec_time_list.append(exec_time_dict[orig_key])
            mean_accuracy_dict[key] = sum(accuracy_list) / len(accuracy_list)
            stddev_accuracy_dict[key] = statistics.stdev(accuracy_list)
            mean_load_time_dict[key] = sum(load_time_list) / len(load_time_list)
            stddev_load_time_dict[key] = statistics.stdev(load_time_list)
            mean_exec_time_dict[key] = sum(exec_time_list) / len(exec_time_list)
            stddev_exec_time_dict[key] = statistics.stdev(exec_time_list)
    print("mean accuracy")
    print(mean_accuracy_dict)
    print("std accuracy")
    print(stddev_accuracy_dict)
    print("mean load time")
    print(mean_load_time_dict)
    print("std load time")
    print(stddev_load_time_dict)
    print("mean exec time")
    print(mean_exec_time_dict)
    print("std exec time")
    print(stddev_exec_time_dict)

    kmeans_csv = open("results/kmeans.csv", "a+")
    agg_csv = open("results/agglomerative.csv", "a+")
    kmeans_csv.write("Number of clusters,Accuracy,Load,Execution" + os.linesep)
    agg_csv.write("Number of clusters,Accuracy,Load,Execution" + os.linesep)
    for key in mean_accuracy_dict:
        csv_fd = None
        if key[0] == "kmeans":
            csv_fd = kmeans_csv
        elif key[0] == "agglomerative":
            csv_fd = agg_csv
        csv_fd.write(str(key[1]) + "," + str(mean_accuracy_dict[key]) + "," + str(mean_load_time_dict[key])\
        + "," + str(mean_exec_time_dict[key]) + os.linesep)


if __name__ == "__main__":
    main()
