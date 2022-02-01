# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:46:31 2021

@author: mathe
"""

import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/khitat_shidda_mihan.csv")

terms_df = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/terms_resources/terms_list.csv").values.tolist()
dates_df = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/terms_resources/dates_list.csv").values.tolist()

dates = {}
for row in dates_df:
    for d in range(row[0], row[1]):
        dates["@YY" + str(d)] = {"label": str(d), "cat": row[2]}

terms = {}
for row in terms_df:
    terms[row[0]] = {"label": row[1], "cat": row[2]}    

heads = data.columns.values.tolist()
for head in ["section", "st_pos", "mid_pos"]:
    heads.remove(head)

fig, axs = plt.subplots(3, 1, sharex = True, sharey = False)
fig.set_size_inches(20, 12)
# plt.plot("mid_pos", "@YY806", linestyle = '-', data = data, label="806", alpha = 0.8, linewidth = 0.7)
# plt.plot("mid_pos", "@YY807", linestyle = '-', data = data, label="807", alpha = 0.6, linewidth = 0.7)
for column in heads:
    if re.match(r"@YY\d{3}", column):
        item = dates[column]
        if item["cat"] == "Events of 806":
            axs[2].plot("mid_pos", column, linestyle = '-', data = data, label=item["label"], alpha = 0.6, linewidth = 0.7)
        if item["cat"] == "Fatimid Fitna":
            axs[1].plot("mid_pos", column, linestyle = '-', data = data, label=item["label"], alpha = 0.6, linewidth = 0.7)
    else:
        if column in terms.keys():
            item = terms[column]
            if item["cat"] == "Events of 806":
                axs[2].plot("mid_pos", column, linestyle = '-', data = data, label=item["label"], alpha = 0.6, linewidth = 0.7)
            if item["cat"] == "Fatimid Fitna":
                axs[1].plot("mid_pos", column, linestyle = '-', data = data, label=item["label"], alpha = 0.6, linewidth = 0.7)
            if item["cat"] == "Destruction/Loss":
                axs[0].plot("mid_pos", column, linestyle = '-', data = data, label=item["label"], alpha = 0.6, linewidth = 0.7)
        else:
            print(column + " not found in df")
    
# plt.vlines("st_pos", ymin = -1, ymax = 0, colors= 'black', data=data, linewidth = 0.2, label = "Section\nboundary")


# data_list = data[["st_pos", "Topic_id"]].values.tolist()
# for row in data_list:
#     if row[1] != 0:
#         plt.vlines(row[0], 0, 10, label = "Topic: " + str(row[1]), linewidth = 0.7, linestyle = ':', color = 'red')
        

axs[0].legend(title = "Term relating to loss or destruction", loc = "upper left", ncol=8)
axs[1].legend(title = "Term relating to Fatimid fitna", loc = "upper left", ncol=8)
axs[2].legend(title = "Term relating to events of 806", loc = "upper left", ncol=8)
plt.xlabel("Number of words into the Khiṭaṭ")
fig.text(0.06, 0.5, 'Number of mentions of terms in section', ha='center', va='center', rotation='vertical')

# axs[0].set_ylabel("Number of mentions of terms related to loss or destruction")
# axs[1].set_ylabel("Number of mentions of terms related to Fatimid fitna")
# axs[2].set_ylabel("Number of mentions of terms related to events of 806")



plt.savefig("Khitat_Terms_ppt.png", dpi=300, bbox_inches = "tight")

plt.show


