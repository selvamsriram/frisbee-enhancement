import re
import json
import datetime
import functools as ft
import requests
from elasticsearch import Elasticsearch
from pprint import pprint

# Global definitions
# None now.

#------------------------------------------------------------------------------
# Prints all messages to screen
def dump_all_messages (hits, filename):
  length = len(hits)
  if (filename != None):
    f_handle = open (filename, "w")

  for i in range (0, length):
    if (filename != None):
      #f_handle.write (hits[i]["_source"]["@timestamp"] + " : " + hits[i]["_source"]["message"] + "\n")
      f_handle.write (hits[i]["_source"]["message"] + "\n")
    else:
      print (hits[i]["_source"]["@timestamp"], hits[i]["_source"]["message"])

#------------------------------------------------------------------------------
# Preprocess master function
def begin_preprocess (data, filename):
  if data == None:
    return
  
  #Debug dump
  dump_all_messages (data, filename)

#------------------------------------------------------------------------------
def is_no_timestamp (hit):
  if "timestamp" not in hit["_source"]:
    return True 
  elif hit["_source"]["timestamp"] == None:
    return True 
  return False 

#------------------------------------------------------------------------------
# Collect data per node from Kibana
def collect_data_per_node (es, image_name):
  query_str = "(source:frisbeed.log) AND beat.hostname: boss.utah.cloudlab.us"
  data = es.search(index="_all", scroll = '2m', body = 
        {
         "query": {
                   "bool": { 
                            "must": [
                                     { "match": { "source":   "frisbeed.log"}}, 
                                     { "match": { "beat.hostname": "boss.utah.cloudlab.us" }}
                                    ],
                            "filter": [ 
                                     { "range": { "@timestamp": { "gte": "2019-02-07", "time_zone": "-06:00"}}}
                                      ]
                          }
                },
         "sort" : [
                  { "@timestamp": {"order": "asc"}},
                  { "offset": {"order": "asc"}}
                  ],
         "size": 10000,
       })
  sid = data['_scroll_id']
  scroll_size = (data['hits']['total'])

  # Save retrieved information
  dst_list = []
  dst_list.extend(data['hits']['hits'])

  print ("Scroll Size : ", scroll_size)
  while scroll_size > 0:
    data = es.scroll(scroll_id=sid, scroll='2m')

    # Update the scroll ID
    sid = data['_scroll_id']

    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])
    print ("Scroll Size : ", scroll_size)
    dst_list.extend(data['hits']['hits'])

  return dst_list

#------------------------------------------------------------------------------
# Main function starts here
es  = Elasticsearch()
collected_data = collect_data_per_node (es, "IMAGE_NAME")
print ("Collected total lines :", len(collected_data))

# Start the processing and dumping of log messages.
begin_preprocess (collected_data, "messages.log")  #Write to file
#begin_preprocess (collected_data, None)           #Write to stdout
