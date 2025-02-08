#most of the code here has been inspired from the assignment's example

#importing section

import os
from os.path import dirname
from parser import *
from preprocessing import *
from indexing import *
from search import *
from weighting_methods import *
from utils import *
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

    # testing - build inverted index
    inverted_index = invert_index(documents)

    weight_method = BM25(inverted_index, doc_lengths=collect_doc_lengths(documents))
    search_e = SearchEngine(weight_method, similarity_measure="cos_sim")
    search_e.search(pair_usable_query(queries))

    print(search_e.results['9'])
    "save_output(search_e.results,path)" #replace path for the path you want the output results in
    "save_inv_index(inverted_index,path)" #replace path for the path you want the inverted index in
    #once you have replaced the paths you can put the functions in the code

#save the output
def save_output(main_output,path): #inverted index we want to save, path to the file location
    with open(path, 'w', encoding='utf-8') as file: #open a file at the path location
        json.dump(main_output, file, indent=4) #put the output in the file

#load a previous output that has been saved
def load_output(path): #file path
    with open(path, 'r', encoding='utf-8') as file: #open the file at the path location
        prev_output=json.load(file) #previous output is the content of the file
    return prev_output


if __name__ == "__main__":
    main()
