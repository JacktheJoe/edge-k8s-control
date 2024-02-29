import csv
import os
import time
import pandas as pd

networklog = os.environ.get('NETWORK_LOG')
metriclog = os.environ.get('METRIC_LOG')
decisionlog = os.environ.get('DECISION_LOG')

decision_interval = int(os.environ.get('DECISION_INTERVAL'))

# TODO: update decision

# hard requirements for network readings
latency_max = 50
bw_min = 100

def merge_cluster_info():
    
    cluster_info_df = pd.read_csv(networklog)
    metric_log_df = pd.read_csv(metriclog)
    
    filtered_clusters_df = cluster_info_df[(cluster_info_df['latency'] <= latency_max) & (cluster_info_df['bandwidth'] >= bw_min)]
    
    merged_df = pd.merge(filtered_clusters_df, metric_log_df, on='cluster_id', how='inner')
    
    # will return a filtered list of cluster information
    return merged_df.to_dict('records')

def decision_logic():
    clusters = []
    filtered_clusters = merge_cluster_info()
    for cluster_id, details in filtered_clusters.items():
        cpu = details['cpu']
        ram = details['ram']
        clusters.append((cluster_id, cpu, ram))
    
    # Rank clusters based on the lowest average of CPU and RAM
    ranked_clusters = sorted(clusters, key=lambda x: (x[1] + x[2]) / 2)
    
    # Select the best cluster
    best_cluster_id = ranked_clusters[0][0] if ranked_clusters else None

    # Overwrite the decisionlog file with the best cluster's cluster_id
    with open(decisionlog, 'w') as file:
        if best_cluster_id:
            file.write(best_cluster_id)
            print(f"Best target '{best_cluster_id}' -> {decisionlog}.")
        else:
            print("No cluster to save.")
    
    return best_cluster_id

if __name__ == '__main__':
    while True:
        decision_logic()
        time.sleep(decision_interval)