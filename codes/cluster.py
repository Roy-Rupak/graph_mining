import networkx as nx
import pickle
from sklearn import cluster

def clusterize(G_nx, k, clustering_technique = 'k_means'):
    nodes = G_nx.nodes(data=True)
    coordinate_list = [[nodes[i]['x'], nodes[i]['y']] for i in range(len(nodes))]
    num_clusters = k

    if clustering_technique == 'k_means':
        res = cluster.KMeans(num_clusters).fit(coordinate_list)
    elif clustering_technique == 'agglomerative':
        res=cluster.AgglomerativeClustering(n_clusters=k).fit(coordinate_list) 
    #res= cluster.SpectralClustering(n_clusters=2,random_state=0).fit(coordinate_list)
    # res=nx.clustering(coordinate_list)

    cluster_labels = res.labels_

    node_list_per_cluster = {}
    for id in range(num_clusters):
        node_list_per_cluster[id] = []

    node_id = 0
    for cluster_label in cluster_labels:
        node_list_per_cluster[cluster_label].append(node_id)
        node_id += 1

    return cluster_labels, node_list_per_cluster

def construct_subgraphs(G_nx, num_clusters, cluster_labels, node_list_per_cluster):
    subgraph_dict = {}
    for cluster_id in range(num_clusters):
        subgraph_dict[cluster_id] = nx.Graph()

    gateway_dict = {}
    nodes = G_nx.nodes(data=True)
    edges = G_nx.edges(data=True)

    for cluster_id in node_list_per_cluster:
        node_ids = node_list_per_cluster[cluster_id]
        for node_id in node_ids:
            subgraph_dict[cluster_id].add_node(node_id, attr_dict=nodes[node_id])

    for node_i, node_j, edge_info in edges:
        if cluster_labels[node_i] == cluster_labels[node_j]:
            subgraph_dict[cluster_labels[node_i]].add_edge(node_i, node_j, attr=edge_info)
        else:
            gateway_dict[(cluster_labels[node_i], cluster_labels[node_j], node_i, node_j)] = edge_info

    return subgraph_dict, gateway_dict

def dump_as_pickle(output_dir, cluster_labels, subgraph_dict, gateway_dict, gateway_graph):
    with open(output_dir+'/cluster_labels.pickle', 'wb') as handle:
        pickle.dump(cluster_labels, handle, protocol=pickle.HIGHEST_PROTOCOL)

    for cluster_id in subgraph_dict:
        with open(output_dir+'/file'+str(cluster_id)+'.pickle', 'wb') as handle:
            pickle.dump(subgraph_dict[cluster_id], handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(output_dir+'/gateways.pickle', 'wb') as handle:
        pickle.dump(gateway_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open(output_dir+'/gateway_graph.pickle', 'wb') as handle:
        pickle.dump(gateway_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
