# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 12:57:56 2021

@author: mathe
"""

import pandas as pd
import os
from tqdm import tqdm

path = "C:/Users/mathe/Documents/Github repos/fitna-study/dates_analysis/date_freqs"
out_dir = "C:/Users/mathe/Documents/Github repos/fitna-study/dates_analysis/25y_freqs"
os.chdir(path)

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        csv_path = os.path.abspath(os.path.join(root, name))
        df = pd.read_csv(csv_path).values.tolist()
        print(name)
        out = []
        for date in tqdm(df):
            
            new_line = date[:]
            date_str = str(date[0])
            if len(date_str) == 2:
                date_str = "0" + date_str
            elif len(date_str) == 1:
                date_str = "00" + date_str
            century = int(date_str[0] + "00")
            if date_str == "000":
                continue            
            elif int(date_str[1:3]) <= 25:
                y25 = century + 25              
            elif int(date_str[1:3]) <= 50:
                y25 = century + 50                
            elif int(date_str[1:3]) <= 75:
                y25 = century + 75
            else:
                if century == 0:
                        y25 = 100
                else:
                    y25 = century + 100
            new_line.append(str(y25))
            
            out.append(new_line)
        
        out_df = pd.DataFrame(out, columns = ["date", "freq", "25-y"])
        out_path = os.path.abspath(os.path.join(out_dir, name + "_25y.csv"))
        out_df.to_csv(out_path, index=False)
            
            
            
                