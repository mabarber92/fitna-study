# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 12:12:48 2021

@author: mathe
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def add_data_labels(ax, offset = 10):
    for p in ax.patches:
        height = p.get_height() # get the height of each bar
        # adding text to each bar
        ax.text(x = p.get_x()+(p.get_width()/2), y = height+offset, s = "{:.0f}".format(height), ha = "center")
    return ax


muq_dates = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/25y_freqs/0845Maqrizi.Muqaffa.Shamela19Y0145334-ara1.dates_tagged.all_dates_distinct.csv_25y.csv")
khit_dates = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/25y_freqs/0845Maqrizi.Mawaciz.Shamela0011566-ara1.completed.dates_tagged.all_dates_distinct.csv_25y.csv")
ittiaz_dates = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/25y_freqs/0845Maqrizi.ItticazHunafa.Shamela0000176-ara1.completed.dates_tagged.all_dates_distinct.csv_25y.csv")
suluk_dates = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/25y_freqs/0845Maqrizi.Suluk.Shamela0006667-ara1.completed.dates_tagged.all_dates_distinct.csv_25y.csv")

fig, axs = plt.subplots(4, 1, sharex=True, sharey=True)
fig.set_size_inches(20, 10)

ax0 = sns.barplot(data = muq_dates, x="25-y", y="freq", estimator = np.sum, ci=None, ax=axs[0])
add_data_labels(ax0)
ax1 = sns.barplot(data = khit_dates, x = "25-y", y="freq", estimator = np.sum, ci=None, ax=axs[1])
add_data_labels(ax1)
ax2 = sns.barplot(data = ittiaz_dates, x = "25-y", y="freq", estimator = np.sum, ci=None, ax=axs[2])
add_data_labels(ax2)
ax3 = sns.barplot(data = suluk_dates, x = "25-y", y="freq", estimator = np.sum, ci=None, ax=axs[3])
add_data_labels(ax3)


plt.xticks(rotation=90)
axs[0].set_xlabel("")
axs[1].set_xlabel("")
axs[2].set_xlabel("")
axs[3].set_xlabel("Years - 25 year spans")

axs[0].set_ylabel("Muqaffa frequency")
axs[1].set_ylabel("Khitat frequency")
axs[2].set_ylabel("Ittiaz frequency")
axs[3].set_ylabel("Suluk frequency")

plt.savefig("C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/figures/maq_comp.png", dpi=300)


plt.show()