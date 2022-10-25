The outputs in this folder were produced by running:

count_variations.py

With the regex:

.?يوسف


Full settings:

```
phrase_list = [".?يوسف"]

corpus_base_path = "/corpus_10_21/"
metadata_path = "/OpenITI_metadata_2021-2-5.csv"
out = "Yusuf_search/variation_counts1.csv"
total = "Yusuf_search/total_counts1.csv"
gram2 = "Yusuf_search/total_2grams.csv"
gram3 = "Yusuf_search/total_3grams.csv"
results_path = "Yusuf_search/all_results.csv"

results = capture_phrases(phrase_list, corpus_base_path, metadata_path, pre_capture = 9, post_capture = 20)
results.to_csv(results_path, encoding = "utf-8-sig", index = False)
count_token_similarities(results, out, total, gram2, gram3)

```
