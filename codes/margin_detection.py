import data_import as di
import networkx as nx
import osmnx as ox
from sklearn import cluster
from sklearn import metrics
#Get NetworkX grapg
G_nx = di.get_graph_from_place("Tallahassee, Florida")

nodes = G_nx.nodes(data=True)

coordinate_list = [[nodes[i]['x'], nodes[i]['y']] for i in range(len(nodes))]
num_clusters = 8

res = cluster.KMeans(num_clusters).fit(coordinate_list)
cluster_centers = res.cluster_centers_
cluster_labels = res.labels_

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



print(len(silhouette_labels))
print(silhouette_info)

