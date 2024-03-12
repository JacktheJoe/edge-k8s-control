# HELP container_cpu_usage_seconds_total [ALPHA] Cumulative cpu time consumed by the container in core-seconds
# TYPE container_cpu_usage_seconds_total counter
container_cpu_usage_seconds_total{container="calico-node",namespace="kube-system",pod="calico-node-8mtdh"} 109.079522718 1710222816920
container_cpu_usage_seconds_total{container="kube-proxy",namespace="kube-system",pod="kube-proxy-q4dks"} 1.664876373 1710222820860
# HELP container_memory_working_set_bytes [ALPHA] Current working set of the container in bytes
# TYPE container_memory_working_set_bytes gauge
container_memory_working_set_bytes{container="calico-node",namespace="kube-system",pod="calico-node-8mtdh"} 1.34934528e+08 1710222816920
container_memory_working_set_bytes{container="kube-proxy",namespace="kube-system",pod="kube-proxy-q4dks"} 1.5761408e+07 1710222820860
# HELP container_start_time_seconds [ALPHA] Start time of the container since unix epoch in seconds
# TYPE container_start_time_seconds gauge
container_start_time_seconds{container="calico-node",namespace="kube-system",pod="calico-node-8mtdh"} 1.7102115924097388e+09 1710211592409
container_start_time_seconds{container="kube-proxy",namespace="kube-system",pod="kube-proxy-q4dks"} 1.710211558868e+09 1710211558868
# HELP node_cpu_usage_seconds_total [ALPHA] Cumulative cpu time consumed by the node in core-seconds
# TYPE node_cpu_usage_seconds_total counter
node_cpu_usage_seconds_total 254.050927655 1710222817924
# HELP node_memory_working_set_bytes [ALPHA] Current working set of the node in bytes
# TYPE node_memory_working_set_bytes gauge
node_memory_working_set_bytes 8.63531008e+08 1710222817924
# HELP pod_cpu_usage_seconds_total [ALPHA] Cumulative cpu time consumed by the pod in core-seconds
# TYPE pod_cpu_usage_seconds_total counter
pod_cpu_usage_seconds_total{namespace="kube-system",pod="calico-node-8mtdh"} 109.884274716 1710222825432
pod_cpu_usage_seconds_total{namespace="kube-system",pod="kube-proxy-q4dks"} 1.678078315 1710222821302
# HELP pod_memory_working_set_bytes [ALPHA] Current working set of the pod in bytes
# TYPE pod_memory_working_set_bytes gauge
pod_memory_working_set_bytes{namespace="kube-system",pod="calico-node-8mtdh"} 4.27851776e+08 1710222825432
pod_memory_working_set_bytes{namespace="kube-system",pod="kube-proxy-q4dks"} 1.5949824e+07 1710222821302
# HELP pod_swap_usage_bytes [ALPHA] Current amount of the pod swap usage in bytes. Reported only on non-windows systems
# TYPE pod_swap_usage_bytes gauge
pod_swap_usage_bytes{namespace="kube-system",pod="calico-node-8mtdh"} 0 1710222825432
pod_swap_usage_bytes{namespace="kube-system",pod="kube-proxy-q4dks"} 0 1710222821302
# HELP scrape_error [ALPHA] 1 if there was an error while getting container metrics, 0 otherwise
# TYPE scrape_error gauge
scrape_error 0


# HELP container_cpu_usage_seconds_total [ALPHA] Cumulative cpu time consumed by the container in core-seconds
# TYPE container_cpu_usage_seconds_total counter
container_cpu_usage_seconds_total{container="calico-node",namespace="kube-system",pod="calico-node-4k872"} 118.100095323 1710222875902
container_cpu_usage_seconds_total{container="kube-proxy",namespace="kube-system",pod="kube-proxy-rz4nt"} 1.848492079 1710222886628
container_cpu_usage_seconds_total{container="metrics-server",namespace="kube-system",pod="metrics-server-7c94c94795-fskp9"} 8.394812803 1710222877784
# HELP container_memory_working_set_bytes [ALPHA] Current working set of the container in bytes
# TYPE container_memory_working_set_bytes gauge
container_memory_working_set_bytes{container="calico-node",namespace="kube-system",pod="calico-node-4k872"} 1.69046016e+08 1710222875902
container_memory_working_set_bytes{container="kube-proxy",namespace="kube-system",pod="kube-proxy-rz4nt"} 1.4835712e+07 1710222886628
container_memory_working_set_bytes{container="metrics-server",namespace="kube-system",pod="metrics-server-7c94c94795-fskp9"} 1.4942208e+07 1710222877784
# HELP container_start_time_seconds [ALPHA] Start time of the container since unix epoch in seconds
# TYPE container_start_time_seconds gauge
container_start_time_seconds{container="calico-node",namespace="kube-system",pod="calico-node-4k872"} 1.710211561028e+09 1710211561028
container_start_time_seconds{container="kube-proxy",namespace="kube-system",pod="kube-proxy-rz4nt"} 1.71021155838e+09 1710211558380
container_start_time_seconds{container="metrics-server",namespace="kube-system",pod="metrics-server-7c94c94795-fskp9"} 1.7102160253231318e+09 1710216025323
# HELP node_cpu_usage_seconds_total [ALPHA] Cumulative cpu time consumed by the node in core-seconds
# TYPE node_cpu_usage_seconds_total counter
node_cpu_usage_seconds_total 290.484058038 1710222883610
# HELP node_memory_working_set_bytes [ALPHA] Current working set of the node in bytes
# TYPE node_memory_working_set_bytes gauge
node_memory_working_set_bytes 7.64698624e+08 1710222883610
# HELP pod_cpu_usage_seconds_total [ALPHA] Cumulative cpu time consumed by the pod in core-seconds
# TYPE pod_cpu_usage_seconds_total counter
pod_cpu_usage_seconds_total{namespace="kube-system",pod="calico-node-4k872"} 118.790975767 1710222884006
pod_cpu_usage_seconds_total{namespace="kube-system",pod="kube-proxy-rz4nt"} 1.862934217 1710222882885
pod_cpu_usage_seconds_total{namespace="kube-system",pod="metrics-server-7c94c94795-fskp9"} 8.413299567 1710222884006
# HELP pod_memory_working_set_bytes [ALPHA] Current working set of the pod in bytes
# TYPE pod_memory_working_set_bytes gauge
pod_memory_working_set_bytes{namespace="kube-system",pod="calico-node-4k872"} 1.69283584e+08 1710222884006
pod_memory_working_set_bytes{namespace="kube-system",pod="kube-proxy-rz4nt"} 1.4999552e+07 1710222882885
pod_memory_working_set_bytes{namespace="kube-system",pod="metrics-server-7c94c94795-fskp9"} 1.5130624e+07 1710222884006
# HELP pod_swap_usage_bytes [ALPHA] Current amount of the pod swap usage in bytes. Reported only on non-windows systems
# TYPE pod_swap_usage_bytes gauge
pod_swap_usage_bytes{namespace="kube-system",pod="calico-node-4k872"} 0 1710222884006
pod_swap_usage_bytes{namespace="kube-system",pod="kube-proxy-rz4nt"} 0 1710222882885
pod_swap_usage_bytes{namespace="kube-system",pod="metrics-server-7c94c94795-fskp9"} 0 1710222884006
# HELP scrape_error [ALPHA] 1 if there was an error while getting container metrics, 0 otherwise
# TYPE scrape_error gauge
scrape_error 0
