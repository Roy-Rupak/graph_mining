import experiment
import os
import random
import sys

def generate_hosts(num_of_processes, host_prefix, init_hosts, init_host_id):
    max_host_id = init_host_id + num_of_processes - 1
    hosts = init_hosts
    host_id = init_host_id + 1
    while host_id <= max_host_id:
        current_host = host_prefix + str(host_id)
        hosts += ("," + current_host)
        host_id += 1
    return hosts


def main():
    host_prefix = 'inv'
    init_host_id = 32
    init_hosts = host_prefix + str(init_host_id)
    number_of_nodes = 39157 # now hard-coded for Tallahassee
    output_file = sys.argv[1]

    clustering_techniques = ['kmeans', 'agglomerative']
    for clustering_technique in clustering_techniques:
        print(clustering_technique + " clustering")
        max_num_clusters = 8
        number_of_random_runs = 10
        for iteration in range(number_of_random_runs):
            source, dest = random.sample(range(number_of_nodes),2)
            num_clusters = 1
            while num_clusters <= max_num_clusters:
                print("running for " + str(num_clusters) + " clusters...")
                num_of_processes = num_clusters
                hosts = generate_hosts(num_of_processes, host_prefix, init_hosts, init_host_id)
                clusters_dir = "clusters/" + clustering_technique + "/tallahassee_k" + str(num_clusters)
                cmd = "mpiexec -hosts " + str(hosts) + " -n " + str(num_of_processes) + \
                    " python experiment.py " + clusters_dir + " " + str(source) + " " + \
                    str(dest) + " " + clustering_technique + " " + str(num_clusters) + \
                    " " + str(iteration) + " " + output_file
                os.system(cmd)
                print("end run for " + str(num_clusters) + " clusters")
                num_clusters *= 2

if __name__ == "__main__":
    main()
