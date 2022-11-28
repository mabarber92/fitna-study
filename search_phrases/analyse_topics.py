# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 13:54:16 2022

@author: mathe
"""

import pandas as pd

# Import df
df_path = "Yusuf_search/topic_model_test_arabertv02_noset_withinfo.csv"
df = pd.read_csv(df_path)

# Split df by topics and sort
df[['topic2', 'w1', 'w2', 'w3', 'w4']] = df['Name'].str.split('_', expand=True).iloc[:,0:5]
df = df.sort_values(by=['w1', 'w2', 'w3', 'w4'])
df_info = df[['Topic', 'Name', 'Count', 'w1', 'w2', 'w3', 'w4']]
df_info = df_info.drop_duplicates()
df.drop(columns=['topic', 'topic2', 'Name'])

# Write out df and df containing sorted keys to topics
out_path = "Yusuf_search/topic_model_test_arabertv02_noset_withinfo_sorted.csv"
out_key = "Yusuf_search/topic_model_test_arabertv02_noset_withinfo_key.csv"
df.to_csv(out_path, index = False, encoding = 'utf-8-sig')
df_info.to_csv(out_key, index = False, encoding = 'utf-8-sig')
