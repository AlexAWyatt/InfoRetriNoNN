#most of the code here has been inspired from the assignment's example

#importing section

import os
from os.path import dirname
from parser import *
from preprocessing import *
from indexing import *
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.stem.snowball import EnglishStemmer

def main():
    # booleans to control parsing
    parse_docs = True
    parse_queries = True

    #dataset logistics
    absolute_base_path = dirname(dirname(__file__))
    dataset = absolute_base_path + "\\data\\scifact" #this is where we will change the dataset that we use
    doc_file_path = dataset + '\\corpus.jsonl'
    query_file_path = dataset + '\\queries.jsonl'

    # Processed files
    index_file_path = absolute_base_path + '\\data\\processed\\inverted_index.json'
    preprocessed_docs_path = absolute_base_path + '\\data\\processed\\preprocessed_docs.json'
    preprocessed_queries_path = absolute_base_path + '\\data\\processed\\preprocessed_queries.json'

    # Define which stopwords list to use
    # load in stopword files - 179 words
    """ nltk.download('stopwords')
    nltk.download('punkt_tab')
    #using a set as it is easier to look up things from (in O(1) as opposed to O(n) from a list)
    stop_words = set(stopwords.words('english')) """

    # read in StopWords List - 779 words
    stop_words = set()
    with open(dataset_dir + "\\StopWords.txt") as file:
        for line in file:
            stop_words.add(line.rstrip())

    
    # Define which stemmer to use
    func_stemmer = PorterStemmer()

    print("Parsing the dataset...")
    documents=[]

    #getting the queries.
    queries = parse_queries_from_file(query_file_path)

    #preprocessing the documents
    if os.path.exists(preprocessed_docs_path) and not parse_docs:
        print("Loading preprocessed documents...")
        documents = load_preprocessed_data(preprocessed_docs_path)
    else:
        print("Preprocessing documents...")
        # change params here to use different stemmer and different stop words list / to not use either
        documents = preprocess_documents(parse_documents_from_file(doc_file_path), removestopwords=True, stopwords=stop_words, stem_text=True, stemmer = func_stemmer)
        save_preprocessed_data(documents, preprocessed_docs_path)

    #Preprocessing the queries if they have not been preprocessed yet
    if os.path.exists(preprocessed_queries_path) and not parse_queries:
        print("Loading preprocessed queries...")
        queries=load_preprocessed_data(preprocessed_queries_path)
    else:
        print("Preprocessing queries...")
        queries = preprocess_queries(parse_queries_from_file(query_file_path), removestopwords=True, stopwords=stop_words, stem_text=True, stemmer = func_stemmer)
        save_preprocessed_data(queries, preprocessed_queries_path)

if __name__ == "__main__":
    main()
