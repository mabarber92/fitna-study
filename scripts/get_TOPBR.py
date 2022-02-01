# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 15:38:51 2021

@author: mathe
"""

import re

path = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/dates_tagged/0845Maqrizi.Mawaciz.Shamela0011566-ara1.completed.dates_tagged.top_br"


with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()
    
first_part = text.split("@TOPBR@")[0]

length = len(re.split(r"\s", first_part))


print(length)