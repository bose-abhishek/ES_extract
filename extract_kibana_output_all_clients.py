import sys
import json
import time
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth

user = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]
env = sys.argv[4]

#Creating Kibana query string using user input

kibana_query="""\
{{ \n
"from" : 0, "size" : 10000,\n
"sort": [\n
    {{\n
      "timestamp_end": {{\n
        "order": "asc",\n
        "unmapped_type": "boolean"\n
      }}\n
    }}\n
  ],\n
"query": {{\n
        "bool": {{\n
          "must": [\n
            {{\n
              "range": {{\n
                "timestamp_end": {{\n
                  "gte": "{start_time}",\n
                  "lte": "{end_time}"\n
                }}\n
              }}\n
            }},\n
            {{\n
              "match": {{\n
                "user": "{user}"\n
              }}\n
            }}\n
          ]\n
        }}\n
      }}\
}}\
""".format(start_time=start_time, end_time=end_time, user=user)

#Generating URL based on user input and getting response

if env == "prod":
    url = '<URL>/ripsaw-fio-results*/_search?pretty=true'
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response = requests.post(url, auth=("admin", "<password>"), data=kibana_query, headers=headers)
    print("From Prodution Kibana DB")
elif env == "dev":
    url = '<URL>/ripsaw-fio-results*/_search?pretty=true'
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response = requests.post(url, data=kibana_query, headers=headers)
    print("From Development Kibana DB")
    
kibana_output =  json.loads(response.text)

#print(response)        #for debugging
#print(kibana_output)   #for debugging

print("uuid                                  timestamp_end       sample     servers     bs      numjobs  iodepth  filesize  rd_bw(MB/s)    rd_iops  wr_bw(MB/s)      wr_iops        jobname   clat_rd_mean_ms clat_wr_mean_ms")

for data in kibana_output['hits']['hits']:
    ts = str(data['_source']['timestamp_end'])
    ts_mod = ts[:10]
    #print(ts_mod)
    #print(datetime.fromtimestamp(int(ts_mod)))
    if data['_source']['fio']['jobname'] == "All clients":

        print(data['_source']['uuid'],
            datetime.fromtimestamp(int(ts_mod)),
            "{:6d}".format(data['_source']['sample']),
            "{:>9s}".format(str(len(data['_source']['hosts']))),
            "{:>9s}".format(data['_source']['global_options']['bs']),
            "{:>9s}".format(data['_source']['global_options']['numjobs']),
            "{:>9s}".format(data['_source']['global_options']['iodepth']),
            "{:>9s}".format(data['_source']['global_options']['size']),
            "{:>12.2f}".format(data['_source']['fio']['read']['bw']/1024),
            "{:>12.2f}".format(data['_source']['fio']['read']['iops']),
            "{:>12.2f}".format(data['_source']['fio']['write']['bw']/1024),
            "{:>12.2f}".format(data['_source']['fio']['write']['iops']),
            "{:>14s}".format(data['_source']['fio']['jobname']),
            "{:>12.2f}".format(data['_source']['fio']['read']['clat_ns']['mean']/1000000),
            "{:>12.2f}".format(data['_source']['fio']['write']['clat_ns']['mean']/1000000))

