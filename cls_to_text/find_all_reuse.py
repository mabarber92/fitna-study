# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:44:29 2022

@author: mathe
"""

import os
import pandas as pd
from tqdm import tqdm

def find_all_reuse(msList, reuseDir, metaPath, maxDate = 900):
    
    metaDf = pd.read_csv(metaPath, sep="\t")[["id", "book", "date"]]
    metaDf = metaDf[metaDf["date"] <= maxDate]
    allData = pd.DataFrame()
    os.chdir(reuseDir)
    for root, dirs, files in os.walk(".", topdown=False):
            for name in tqdm(files):
                pairId = name.split("_")[1].split("-")[0]
                meta = metaDf[metaDf["id"] == pairId]
                if len(meta) != 0:
                    reusePath = os.path.join(root, name)
                    print(reusePath)
                    reuseDf = pd.read_csv(reusePath, sep="\t")
                    msReuse = reuseDf[reuseDf['seq1'].isin(msList)]                
                    allData = pd.concat([allData, msReuse])
                else:
                    continue
    allData["id"] = allData["id2"].str.split("-").str[0]
    allData = pd.merge(allData, metaDf, how = "inner", on ="id")
    
    return allData


reuseDir = "D:/Corpus Stats/2021/pairwise-files/Shamela0011566-ara1.completed"
metaPath = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
msList = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/cls_to_text/outputs/0845Maqrizi.Mawaciz.Shamela0011566-ara1_no-clusters.csv")["milestone"].str.split("ms").str[-1].astype(int).to_list()
print(msList)

outDf = find_all_reuse(msList, reuseDir, metaPath)
