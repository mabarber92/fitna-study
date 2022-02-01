# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 12:12:48 2021

@author: mathe
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/scripts/muq_bio_dates.csv")[["25-y", "w_count", "Name"]]
all_dates = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/25y_freqs/0845Maqrizi.Muqaffa.Shamela19Y0145334-ara1.dates_tagged.all_dates_distinct.csv_25y.csv")


fig, axs = plt.subplots(3, 1, sharex = True)
fig.set_size_inches(20, 10)

sns.barplot(data = all_dates, x="25-y", y="freq", estimator = np.sum, ci=None, ax=axs[0]) 
sns.barplot(data = data, x = "25-y", y="w_count", estimator = np.sum, ci=None, ax=axs[1])
sns.countplot(data = data, x = "25-y", ax=axs[2])

plt.xticks(rotation=90)
axs[0].set_ylabel("Number of dates")
axs[1].set_ylabel("Number of words\n in sections")
axs[2].set_ylabel("Number of sections\n with death date")
axs[0].set_xlabel("")
axs[1].set_xlabel("")
axs[2].set_xlabel("Years - 25 year spans")

plt.savefig("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/figures/muq_ppt.png", dpi=300)


plt.show()