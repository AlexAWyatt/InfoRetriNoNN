#most of the code here has been inspired from the assignment's example

#importing section

import os
from os.path import dirname
from parser import *
from preprocessing import *

#dataset logistics - someone please check this
absolute_base_path = dirname(dirname(__file__))
dataset = absolute_base_path + "\\data\\scifact" #this is where we will change the dataset that we use
doc_file_path = dataset + '\\corpus.jsonl'
query_file_path = dataset + '\\queries.jsonl'
#to be built
index_folder_path = absolute_base_path + '\\data\\processed\\inverted_index.json'
preprocessed_docs_path = absolute_base_path + '\\data\\processed\\preprocessed_docs.json'
preprocessed_queries_path = absolute_base_path + '\\data\\processed\\preprocessed_queries.json'

print("Parsing the dataset...")
documents=[]

#getting the queries.
queries = parse_queries_from_file(query_file_path)

#preprocessing the documents
if os.path.exists(preprocessed_docs_path):
    print("Loading preprocessed documents...")
    documents = load_preprocessed_data(preprocessed_docs_path)
else:
    print("Preprocessing documents...")
    documents = preprocess_documents(parse_documents_from_file(doc_file_path))
    save_preprocessed_data(documents, preprocessed_docs_path)

#Preprocessing the queries if they have not been preprocessed yet
if os.path.exists(preprocessed_queries_path):
    print("Loading preprocessed queries...")
    queries=load_preprocessed_data(preprocessed_queries_path)
else:
    print("Preprocessing queries...")
    queries = preprocess_queries(parse_queries_from_file(query_file_path))
    save_preprocessed_data(queries, preprocessed_queries_path)

