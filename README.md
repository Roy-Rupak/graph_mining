# Data Mining Final Project: Towards Clustering Graph Representation of Geographic Dataset for Distributed Systems

## Required Dependencies:

* networkx
* osmnx
* numpy
* pickle
* random
* sklearn
* mpi4py
* sys
* os
* time

#### Dataset used:
* Open Street Map (Currently using data for Tallahassee only)


### Please see the following program for first phase of our computation: clustering and pickle generation

*prepare_clusters.py*

**How to run:**

    python prepare_clusters.py <num_clusters> <clusters_dir> <clustering_technique[k_means | agglomerative]>
    

### Please see the following program for second phase of our computation: Distributed SSSP with Dijkstra's Algorithm

*main.py*

**How to run:**

    # Please log into inv32 node in the Innovation cluster
    python main.py <output_filename>
    * Please see note


### Output format in file:
```
clustering: <clustering technique name>
num_cluster: <Number of clusters>
iteration: <current iteration>
load: <Data loading time>
path: <Shortest path>
exec: <Execution time>
```

#### * NOTE: All codes are run using different combinations of 8 compute nodes in Innovation Cluster (i.e. inv32-39). To exactly reproduce the results you need to have access to the Innovation cluster. Please let us know if you face any issues while running the code and require reproducing the results.
