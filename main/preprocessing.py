"""TODO: Things to make parameters that are decided by driver function
- stopword doc
- stemmer used
- boolean switch for whether to stem words or not (default to stemming on)
- seems like lemmatization doesn't make sense for info retrieval - stick to stemming
"""


#Most of the code here is from the assignement's example.
import json

#imports go here
import os
import nltk #natural language toolkit
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.stem.snowball import EnglishStemmer

relative_dir = os.getcwd()
dataset_dir = relative_dir + "\\data"

nltk.download('stopwords')
nltk.download('punkt_tab')

#using a set as it is easier to look up things from (in O(1) as opposed to O(n) from a list)
stop_words = set(stopwords.words('english'))

# read in Provided StopWords List
stop_words_big = set()
with open(dataset_dir + "\\StopWords.txt") as file:
    for line in file:
        stop_words_big.add(line.rstrip())

#tokenising the texts using nltk's word_tokenize
def tokenize(text):
    tokens = word_tokenize(text.lower())
    return tokens

#stemming each tokens in the list of tokens sent
def stem_tokens(tokens, stemmer = PorterStemmer()):
    return [stemmer.stem(token) for token in tokens]

#??? TODO add comments
def remove_extras(tokens):
    # TODO: figure out origin of these tokens (probably in other processing docs?) - not returned by NLTK - no internet reference
    return [token for token in tokens if token not in ['no_queri','no_narr']]

#preprocessing the text by turning it into "good" tokens
def preprocess_text(text, stem_text = True, stemmer = PorterStemmer()):
    tokens = tokenize(text)

    # If stemming is enabled, stem the tokens with the chosen stemmer
    if stem_text:
        tokens = stem_tokens(tokens, stemmer)
    tokens = remove_extras(tokens)
    return tokens

#preprocessing all of the documents now
def preprocess_documents(documents, stem_text = True, stemmer = PorterStemmer()):
    previous_id = 'x'
    count = 1

    #going through each document line by line and extracting information to tokenise it and put it back where it belongs.
    for doc in documents:
        file_id = str(doc['DOCNO'].split(" ")[0])
        if file_id != previous_id:
            previous_id = file_id
            count += 1
        doc['TEXT'] = preprocess_text(doc['TEXT'], stem_text, stemmer)
        doc['HEAD'] = preprocess_text(doc['HEAD'], stem_text, stemmer)

    return documents

#preprocessing queries
def preprocess_queries(queries, stem_text = True, stemmer = PorterStemmer()):
    for query in queries:
        query['title'] = preprocess_text(query['title'], stem_text, stemmer)
        query['query'] = preprocess_text(query['query'], stem_text, stemmer)
        query['narrative'] = preprocess_text(query['narrative'], stem_text, stemmer)
    return queries

def save_preprocessed_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def load_preprocessed_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data