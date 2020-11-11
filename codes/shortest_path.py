import networkx as nx

def shortest_path_dijkstra(G_nx, source, target):
    shortest_path = nx.dijkstra_path(G_nx, source, target, weight=None)
    return shortest_path

def shortest_paths_dijkstra(G_nx, sources, targets):
    all_pairs_dict = nx.all_pairs_dijkstra(G_nx, weight='length')
    shortest_paths = {}
    for key_i, value_i in all_pairs_dict:
        if key_i in sources:
            print(value_i[key_i])
            for val in value_i:
                print(val)
                # print(value_j[key_j])
                # if key_j in targets:
                #     shortest_paths[(key_i, key_j)] = value_j
                # else:
                #     continue

    # for source in sources:
    #     for target in targets:
    #         print(all_pairs_dict[source][target])

    return shortest_paths

def single_source_paths_dijkstra(G_nx, source, targets):
    single_source_dict = nx.single_source_dijkstra(G_nx, source, weight='length')
    single_source_shortest_paths = []
    print(single_source_dict)

    return single_source_shortest_paths

def multiple_source_paths_dijkstra(G_nx, sources, target):
    single_source_dict = nx.single_source_dijkstra(G_nx, sources, weight='length')
    single_source_shortest_paths = []
    print(single_source_dict)

    return single_source_shortest_paths


def find_point_to_gateway_path(graph, fromnode, gateway_nodes):
    lengths, paths = nx.single_source_dijkstra(graph, fromnode, weight='length')
    gateway_paths =  {k:v for k, v in paths.items() if k in gateway_nodes}
    gateway_lengths =  {k:v for k, v in lengths.items() if k in gateway_nodes}
    return gateway_paths, gateway_lengths


def find_gateway_to_gateway_path(graph, gateway_nodes):
    all_paths = {}
    all_lengths = {}
    for gateway_node in gateway_nodes:
        all_paths[gateway_node], all_lengths[gateway_node] = find_point_to_gateway_path(graph, gateway_node, gateway_nodes)
    return all_paths, all_lengths


def find_gateways_to_gateways_paths(graph, source_gateway_nodes, dest_gateway_nodes):
    all_paths = {}
    all_lengths = {}
    for source_gateway_node in source_gateway_nodes:
        all_paths[source_gateway_node], all_lengths[source_gateway_node] = find_point_to_gateway_path(graph, source_gateway_node, dest_gateway_nodes)
    return all_paths, all_lengths


def find_gateway_to_point_path(graph, tonode, gateway_nodes):
    gateway_paths = {}
    gateway_lengths = {}
    for gateway_node in gateway_nodes:
        lengths, paths = nx.single_source_dijkstra(graph, gateway_node)
        for k, v in paths.items():
            if k == tonode:
                gateway_paths[gateway_node] = v
        for k, v in lengths.items():
            if k == tonode:
                gateway_lengths[gateway_node] = v

    return gateway_paths, gateway_lengths
