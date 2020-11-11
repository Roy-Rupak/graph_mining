from mpi4py import MPI
import networkx as nx
import os
import pickle
import prepare_clusters as pc
import shortest_path as sp
import sys
import time


def read_clusters(clusters_dir, rank):
    cluster_labels = None

    cluster_labels_filename = clusters_dir + "/cluster_labels.pickle"
    with open(cluster_labels_filename, 'rb') as handle:
        cluster_labels = pickle.load(handle)

    gateway_dict = None
    gateway_filename = clusters_dir + "/gateways.pickle"
    with open(gateway_filename, 'rb') as handle:
        gateway_dict = pickle.load(handle)

    gateway_graph = None
    gateway_filename = clusters_dir + "/gateway_graph.pickle"
    with open(gateway_filename, 'rb') as handle:
        gateway_graph = pickle.load(handle)

    subgraph_dict = {}
    internal_connectivity_per_cluster = {}
    internal_lengths_per_cluster = {}
    cluster_filename = clusters_dir + "/file" + str(rank) + ".pickle"
    internal_connectivity_filename = clusters_dir + "/internal" + str(rank) + ".pickle"
    internal_lengths_filename = clusters_dir + "/internal_len" + str(rank) + ".pickle"
    G_nx = None
    with open(cluster_filename, 'rb') as handle:
        G_nx = pickle.load(handle)
    subgraph_dict[rank] = G_nx

    internal_connectivity = None
    with open(internal_connectivity_filename, 'rb') as handle:
        internal_connectivity = pickle.load(handle)
    internal_connectivity_per_cluster[rank] = internal_connectivity

    internal_lengths = None
    with open(internal_lengths_filename, 'rb') as handle:
        internal_lengths = pickle.load(handle)
    internal_lengths_per_cluster[rank] = internal_lengths

    return cluster_labels, subgraph_dict, gateway_dict, internal_connectivity_per_cluster, internal_lengths_per_cluster, gateway_graph


def single_run(clusters_dir, source, dest, clustering_technique, num_clusters, iteration, output_file_path):
    start_time = MPI.Wtime()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    cluster_labels, subgraph_dict, gateway_dict, internal_connectivity_per_cluster, internal_lengths_per_cluster, gateway_graph = read_clusters(clusters_dir, rank)
    if rank == 0:
        with open(output_file_path, 'a+') as output_file:
            output_file.write("clustering:" + clustering_technique + os.linesep)
            output_file.write("num_cluster:" + str(num_clusters) + os.linesep)
            output_file.write("iteration:" + str(iteration) + os.linesep)
            output_file.write("load:" + str(MPI.Wtime()-start_time) + os.linesep)

    paths = None
    lengths = None

    start_time = MPI.Wtime()
    shortest_path = []
    if cluster_labels[source] == cluster_labels[dest]:
        if rank == cluster_labels[source]:
            shortest_path = sp.shortest_path_dijkstra(subgraph_dict[rank], source, dest)
            with open(output_file_path, 'a') as output_file:
                output_file.write("path:" + str(shortest_path) + os.linesep)
                output_file.write("exec:" + str(MPI.Wtime()-start_time) + os.linesep)
            return

    else:
        gateway_nodes_per_cluster = pc.get_gateway_per_cluster(num_clusters, gateway_dict)

        if cluster_labels[source] == rank:
            paths, lengths = sp.find_point_to_gateway_path(subgraph_dict[rank], source, gateway_nodes_per_cluster[rank])
        elif cluster_labels[dest] == rank:
            paths, lengths = sp.find_gateway_to_point_path(subgraph_dict[rank], dest, gateway_nodes_per_cluster[rank])
        else:
            paths = internal_connectivity_per_cluster[rank]
            lengths = internal_lengths_per_cluster[rank]

    final_path = []
    if rank == cluster_labels[source]:
        paths_dict = {}
        lengths_dict = {}
        for i in range(num_clusters):
            if i != rank:
                paths_dict[i], lengths_dict[i] = comm.recv(source=i, tag=i)
            else:
                paths_dict[i] = paths
                lengths_dict[i] = lengths
        gateways_shortest_paths = []
        gateways_lengths = []
        source_gateway_nodes = paths_dict[cluster_labels[source]].keys()
        dest_gateway_nodes = paths_dict[cluster_labels[dest]].keys()
        shortest_paths, shortest_path_lengths = sp.find_gateways_to_gateways_paths(gateway_graph, source_gateway_nodes, dest_gateway_nodes)

        for source_nodes, source_shortest_paths in shortest_paths.items():
            for dest_node, shortest_path in source_shortest_paths.items():
                len_shortest_path = len(shortest_path)
                length = 0
                complete_shortest_path = []
                prev_node = None
                for node_id in range(len_shortest_path):
                    current_node = shortest_path[node_id]
                    if node_id == 0:
                        for item in paths_dict[cluster_labels[source]][current_node]:
                            complete_shortest_path.append(item)
                        length += lengths_dict[cluster_labels[source]][current_node]
                        continue
                    elif node_id == len_shortest_path-1:
                        for item in paths_dict[cluster_labels[dest]][current_node]:
                            complete_shortest_path.append(item)
                        length += lengths_dict[cluster_labels[dest]][current_node]
                    elif prev_node and cluster_labels[prev_node] != cluster_labels[current_node]:
                        complete_shortest_path.append(current_node)
                        length += 1
                    elif prev_node and cluster_labels[prev_node] == cluster_labels[current_node] \
                        and cluster_labels[current_node] != cluster_labels[source] \
                        and cluster_labels[current_node] != cluster_labels[dest]:
                        for item in paths_dict[cluster_labels[current_node]][prev_node][current_node]:
                            complete_shortest_path.append(item)
                            length += 1
                    else:
                        complete_shortest_path.append(current_node)
                        length += 1

                    prev_node = current_node

            gateways_shortest_paths.append(complete_shortest_path)
            gateways_lengths.append(length)

        min_length = min(gateways_lengths)
        final_path = gateways_shortest_paths[gateways_lengths.index(min_length)]

    if rank != cluster_labels[source]:
        comm.send((paths, lengths), dest=cluster_labels[source], tag=rank)
    

    if rank == cluster_labels[source]:
        with open(output_file_path, 'a') as output_file:
            output_file.write("path:" + str(final_path) + os.linesep)
            output_file.write("exec:" + str(MPI.Wtime()-start_time) + os.linesep)


if __name__ == "__main__":
    single_run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], \
        int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
