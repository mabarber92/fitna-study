# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:46:31 2021

@author: mathe
"""

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/ighatha_mihan_pattern_ms.csv")

fig, axs = plt.subplots(1, 1, sharex = True, sharey = True)
fig.set_size_inches(15, 10)
# plt.plot("mid_pos", "@YY806", linestyle = '-', data = data, label="806", alpha = 0.8, linewidth = 0.7)
# plt.plot("mid_pos", "@YY807", linestyle = '-', data = data, label="807", alpha = 0.6, linewidth = 0.7)
plt.plot("mid_pos", "Mihan", linestyle = '-', data = data, label="Mihan", alpha = 0.6, linewidth = 0.7)
# plt.vlines("st_pos", ymin = -1, ymax = 0, colors= 'black', data=data, linewidth = 0.2, label = "Section\nboundary")

# data_list = data[["st_pos", "Topic_id"]].values.tolist()
# for row in data_list:
#     if row[1] != 0:
#         plt.vlines(row[0], 0, 10, label = "Topic: " + str(row[1]), linewidth = 0.7, linestyle = ':', color = 'red')
        

# plt.legend(title = "Term or topic\nnumber", loc = "upper right")
plt.xlabel("Number of words into the Ighatha")
plt.ylabel("Number of mentions of term")
plt.title("Number of mentions of 'Mihan' across the Ighatha")

plt.savefig("Ighatha_mihan_wcounts.png", dpi=300, bbox_inches = "tight")

plt.show


