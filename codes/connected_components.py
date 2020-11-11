import networkx as nx

def get_gateway_edges(gateway_dict):
    edgelist = []
    for key in gateway_dict.keys():
        edgelist.append((key[2], key[3]))
    return edgelist

def generate_gateway_graph(subgraph_dict, gateway_nodes, edgelist):
    for key in gateway_nodes.keys():
        gateways = gateway_nodes[key]
        for i in range(len(gateways)):
            gateway_1 = gateways[i]
            for j in range(len(gateways)):
                gateway_2 = gateways[j]
                if(gateway_1 != gateway_2):
                    if nx.has_path(subgraph_dict[key], gateway_1, gateway_2):
                        edgelist.append((gateway_1, gateway_2))
    
    gateway_graph = nx.DiGraph()
    gateway_graph.add_edges_from(edgelist)

    return gateway_graph 

#res = networkx.all_shortest_paths(G, 1, 3)

