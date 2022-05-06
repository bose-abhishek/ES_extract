# ES_extract
Extract test data from Elastic Search for fio workload.

This code is written specifically for Red Hat internal testing but can be used for other environments as long as following conditions are met:
1. Kibana Elastic Seach is used.
2. Benchmark-operator is used for testing.

Note: You need to add the URL and credentials of the ES server according to your environment.

**Usage**:

$ python3 extract_kibana_output_all_clients.py username start-time end-time environment

start time/end time format: YYYY-MM-DD'T'HH:YY±ZZZZ

environment options: dev|prod

**Example**: 

$ python3 extract_kibana_output_all_clients.py foo 2022-04-06T16:20+0530 2022-04-06T17:20+0530 prod 
