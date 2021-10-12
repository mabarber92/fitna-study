# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 11:17:26 2021

@author: mathe
"""

import os
import re
import pandas as pd

def date_finder(files_path, dates):
    os.chdir(files_path)
    out_list = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            print(name)
            path_e = os.path.join(root, name)
            path = os.path.abspath(path_e)
            
            with open(path, encoding = "utf-8") as f:
                text = f.read()
                f.close()
            for date in dates:
                string = r"\n.*@YY" + str(date) + ".*\n"
                print(string)
                results = re.findall(string, text)
                out_no = len(results)
                print(out_no)
                if out_no >= 1:
                    for result in results:
                        out_list.append([name, date, results])
    
    return pd.DataFrame(out_list, columns = [['text', 'date', 'result']])


path = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/date_tagged_corpus/15_03/dated"

result_806_807 = date_finder(path, [806, 807])