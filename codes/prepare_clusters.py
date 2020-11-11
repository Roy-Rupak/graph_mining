import cluster as cl
import data_import as di
import margin_detection_new as md
import networkx as nx
import numpy as np
import osmnx as ox
import pickle
import shortest_path as sp
import sys

def get_gateway_edges(gateway_dict):
    edgelist = []
    for key in gateway_dict.keys():
        edgelist.append((key[2], key[3], float(gateway_dict[key]['length'])))
    return edgelist

def generate_gateway_graph(subgraph_dict, gateway_nodes, edgelist):
    for key in gateway_nodes.keys():
        gateways = gateway_nodes[key]
        for i in range(len(gateways)):
            gateway_1 = gateways[i]
            for j in range(len(gateways)):
                gateway_2 = gateways[j]
                if(gateway_1 != gateway_2):
                    try:
                        path_length = nx.shortest_path_length(subgraph_dict[key], gateway_1, gateway_2)
                        edgelist.append((gateway_1, gateway_2, path_length))
                    except:
                        dummy = 0

    gateway_graph = nx.Graph()
    gateway_graph.add_weighted_edges_from(edgelist)

    return gateway_graph 

def get_gateway_per_cluster(num_clusters, gateway_dict):
    gateway_dict_per_cluster = {}

    for i in range(num_clusters):
        gateway_dict_per_cluster[i] = []

    for key in gateway_dict.keys():
        if key[2] not in gateway_dict_per_cluster[key[0]]:
            gateway_dict_per_cluster[key[0]].append(key[2])
        if key[3] not in gateway_dict_per_cluster[key[1]]:
            gateway_dict_per_cluster[key[1]].append(key[3])

    return gateway_dict_per_cluster


def initialize_cluster(num_clusters, clusters_dir, clustering_technique):
    # G_nx = di.get_graph_from_osm("dataset/florida.osm/data")
    G_nx = di.get_graph_from_place("Tallahassee, Florida")
    cluster_labels, node_list_per_cluster = cl.clusterize(G_nx, num_clusters, clustering_technique)
    subgraph_dict, gateway_dict = cl.construct_subgraphs(G_nx, num_clusters, cluster_labels, node_list_per_cluster)
    gateways_per_cluster_dict = get_gateway_per_cluster(num_clusters, gateway_dict)
    gateway_edges = get_gateway_edges(gateway_dict)
    gateway_graph = generate_gateway_graph(subgraph_dict, gateways_per_cluster_dict, gateway_edges)

    cl.dump_as_pickle(clusters_dir, cluster_labels, subgraph_dict, gateway_dict, gateway_graph)
    dump_internal_paths(clusters_dir, subgraph_dict, gateways_per_cluster_dict)


def read_clusters(clusters_dir):
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
    for cluster_id in range(2):
        cluster_filename = clusters_dir + "/file" + str(cluster_id) + ".pickle"
        internal_connectivity_filename = clusters_dir + "/internal" + str(cluster_id) + ".pickle"
        G_nx = None
        with open(cluster_filename, 'rb') as handle:
            G_nx = pickle.load(handle)
        subgraph_dict[cluster_id] = G_nx

        internal_connectivity = None
        with open(internal_connectivity_filename, 'rb') as handle:
            internal_connectivity = pickle.load(handle)
        internal_connectivity_per_cluster[cluster_id] = internal_connectivity
    return subgraph_dict, gateway_dict, internal_connectivity_per_cluster, gateway_graph


def dump_internal_paths(clusters_dir, subgraph_dict, gateways_per_cluster_dict):
    internal_gateway_paths = {}
    internal_gateway_lengths = {}
    for cluster_id, gateway_nodes in gateways_per_cluster_dict.items():
        internal_gateway_paths[cluster_id], internal_gateway_lengths[cluster_id] = sp.find_gateway_to_gateway_path(subgraph_dict[cluster_id], gateway_nodes)

        with open(clusters_dir+'/internal'+str(cluster_id)+'.pickle', 'wb') as handle:
            pickle.dump(internal_gateway_paths[cluster_id], handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(clusters_dir+'/internal_len'+str(cluster_id)+'.pickle', 'wb') as handle:
            pickle.dump(internal_gateway_lengths[cluster_id], handle, protocol=pickle.HIGHEST_PROTOCOL)

    return internal_gateway_paths, internal_gateway_lengths


def main():
    if (len(sys.argv) == 4):
        num_clusters = int(sys.argv[1])
        clusters_dir = sys.argv[2]
        clustering_technique = sys.argv[3]
        initialize_cluster(num_clusters, clusters_dir, clustering_technique)
    else:
        print('USAGE:: python prepare_clusters.py <num_clusters> <clusters_dir> <clustering_technique[k_means | agglomerative]>')


if __name__ == "__main__":
    main()
