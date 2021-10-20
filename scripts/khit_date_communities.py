# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 15:47:12 2021

@author: mathe
"""

import networkx as nx
from cdlib import algorithms
from tqdm import tqdm
import json

def comm_detect(dict_list):
    g = nx.Graph()

    for idx, item in enumerate(tqdm(dict_list)):
        g.add_node(item["seq"])
        for comp in dict_list[idx+1:]:
            w = 0
            if item["dates"] == "None":
                
                continue
            for date in item["dates"]:
                if date == "000":
                    
                    continue
                if date in comp["dates"]:
                    w = w + 1
            if w != 0:
                g.add_edge(item["seq"], comp["seq"], weight = w)
    
    comms = algorithms.label_propagation(g)
    return comms
            

path = "C:/Users/mathe/Documents/Github-repos/fitna-study/khit-dates.json"

with open(path) as f:
    data = f.read()
    f.close

dict_list = json.loads(data)

out = comm_detect(dict_list)
    