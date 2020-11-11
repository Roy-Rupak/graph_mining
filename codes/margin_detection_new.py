import data_import as di
import networkx as nx
from sklearn import cluster
from sklearn import metrics


def get_gateways(G_nx, cluster_labels, num_clusters):
    nodes = G_nx.nodes(data=True)

    coordinate_list = [[nodes[i]['x'], nodes[i]['y']] for i in range(len(nodes))]

    silhouette_labels = metrics.silhouette_samples(coordinate_list, cluster_labels, metric='euclidean')


    silhouette_info = {}
    for cluster in range(num_clusters):
        intra_cluster_silhouette = []
        intra_cluster_coordinates = []
        for label in range(len(cluster_labels)):
            if cluster == cluster_labels[label]:
                intra_cluster_silhouette.append(silhouette_labels[label])
                intra_cluster_coordinates.append(coordinate_list[label])
        top_5_index = sorted(range(len(intra_cluster_silhouette)), key = lambda k: intra_cluster_silhouette[k])[-5:]
        silhouette_info[cluster] = [intra_cluster_coordinates[index] for index in top_5_index]

    return silhouette_info
