# -*- coding: utf-8 -*-
"""
Unfinished - need to work on
"""
import pandas as pd

def corpus_tag(df_cl, corpus_path, tagged_out)
    path_list = df_cl.loc[df_cl["from_input"] == True]["local_path"].drop_duplicates().tolist()
    print(path_list)
    for path in tqdm(path_list):
        data_subset = df_out.loc[df_out["local_path"] == path]["id"].drop_duplicates().tolist()
        if type(path) == str:
            path_in = corpus_path + "/" + path.split("../")[-1]
            if os.path.exists(path_in):
                with open(path_in, encoding = "utf-8") as f:
                    text = f.read()
                    f.close()
                book = data_subset[0].split(".")[0]
                for ms_id in data_subset:
                    ms = ms_id.split(".")[-1]
                    clusters = book_dict[book][ms_id]
                    tag = " " + ms
                    for cluster in clusters:
                        tag = tag + " @cl@" + str(cluster) + "@ "
                    text = text.replace(ms, tag)
                out_path = tagged_out + "/" + path.split("/")[-1] + ".cl-tagged"
                with open(out_path, "w", encoding = "utf-8") as f:
                    f.write(text)
                    f.close()
            else:
                print("\nPath: " + path_in + "does not exist - check your specified corpus folder\n")
        else:
            print("\nNo path value for this work, value given: " + path + "\n")

cluster_list = ""
cluster_df = pd.read_csv(cluster_list)