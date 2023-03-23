# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:17:21 2023

@author: mathe
"""

import pandas as pd
from bertopic import BERTopic
# from topically import Topically
from sklearn.cluster import KMeans

from sentence_transformers import SentenceTransformer, models
from torch import nn
import torch



def check_cuda(model):
	if torch.cuda.is_available():
		cuda_device = 0
		model = model.cuda(cuda_device)
	else:
		cuda_device = -1
	return model,cuda_device

def csvToBERTopic(csvIn, csvOut, inputType = "csv", sentenceField = "text", transformer=None, existingModel = None, returnDf = False, returnModel = False, seqLength = 512, 
                  sortBy = ['t1', 't2', 't3', 't4'], embeddingModel = "aubmindlab/bert-base-arabertv02",
                  topicLimit = None):
    
    # Load in input
    if inputType == "csv":
        df = pd.read_csv(csvIn).dropna()
    elif inputType == "df":
        df = csvIn
    
    # Load embedding model
    print("loading model...")
    if not transformer:
        model_name = embeddingModel
        max_seq_length= seqLength
        word_embedding_model = models.Transformer(model_name, max_seq_length)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True)
        dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(), 
                                   out_features=seqLength, 
                                   activation_function=nn.Tanh())
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_model])
        print("model loaded")
        print("checking cuda...")
        model, cuda = check_cuda(model)
    else:
        model = transformer
    
    
    # Take sentence column and pass to encoder
    print("commencing embedding...")
    sentences = df[sentenceField].tolist()
    embeds = model.encode(sentences)
    print("embeds created...")
    
    # Build topic model - if there is a cap on topics initiate topics using KMeans
    if not existingModel:
        if topicLimit:
            print("Using a topicLimit of: " + str(topicLimit))
            cluster_model = KMeans(n_clusters= topicLimit)
            # REVIST - PASS IN CLUSTER MODEL
            topic_model = BERTopic(language = 'multilingual')
        
        else:
            topic_model = BERTopic(language='multilingual')
        
        df['Topic'], probabilities = topic_model.fit_transform(df[sentenceField], embeds)
    else:
        topic_model = existingModel
        df['Topic'], probabilities = topic_model.transform(df[sentenceField], embeds)

    print("clustering and topic model built")

    # fit_transform the model to the sentences and embeddings
    # df['Topic'], probabilities = topic_model.fit_transform(df[sentenceField], embeds)
    
    # Add the topic data to the dataframe
    print("fit_transform complete... adding topic data to df")
    
    topic_info = topic_model.get_topic_info()
    df = df.merge(topic_info, on='Topic', how='left')
    df[["Topic", 't1', 't2', 't3', 't4']] = df["Name"].str.split("_", expand=True)
    df = df.drop(columns=['Name'])
    df = df.sort_values(by=['t1', 't2', 't3', 't4'])

    df.to_csv(csvOut, index=False, encoding='utf-8-sig')
    
    # If returnDf is true - return whole df, if returnModel is true, return the model if both are true return both
    # This allows for function to be fed into following processes without reloading the outputs from storage into memory
    if returnDf:
        return df
    if returnModel:
        return topic_model
    if returnDf and returnModel:
        return df, topic_model