import csv
import os
import time

networklog = os.environ.get('NETWORK_LOG')
metriclog = os.environ.get('METRIC_LOG')
decisionlog = os.environ.get('DECISION_LOG')

decision_interval = int(os.environ.get('DECISION_INTERVAL'))

def fetch_network_metric():
    with open(networklog, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)
    
def fecht_resource_metric():
    pass

def decision_logic():
    # note: since this is currently deployment only no complex logic is used, such as calculating time needed for migrate a size-variing container
    pass