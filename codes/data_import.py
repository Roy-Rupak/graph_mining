import networkx as nx
import osmnx as ox

# returns networkx graph
def get_graph_from_place(place):
    ox.config(use_cache=True, log_console=False)
    G_nx = ox.graph_from_place(place)
    G_nx = nx.relabel.convert_node_labels_to_integers(G_nx)
    return G_nx

# returns networkx graph
def get_graph_from_osm(filename):
    ox.config(use_cache=True, log_console=False)
    G_nx = ox.graph_from_file(filename)
    G_nx = nx.relabel.convert_node_labels_to_integers(G_nx)

    return G_nx
