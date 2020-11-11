import data_import as di
import shortest_path as sp
import time

def main():
    start_time = time.time()
    G_nx = di.get_graph_from_place("Tallahassee, Florida")
    print(time.time()-start_time)
    start_time = time.time()
    # print(sp.shortest_path_dijkstra(G_nx, 100, 33238))
    print(sp.shortest_path_dijkstra(G_nx, 100, 2))
    print(time.time()-start_time)

if __name__ == "__main__":
    main()
