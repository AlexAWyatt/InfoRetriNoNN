#Most of the code here is from the assignement's example.
import json

#imports go here
import nltk #natural language toolkit
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


nltk.download('stopwords')

#using a set as it is easier to look up things from (in O(1) as opposed to O(n) from a list)
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
#print(stop_words)

#tokenising the texts using nltk's word_tokenize
def tokenize(text):
    tokens = word_tokenize(text.lower())
    return tokens

#stemming each tokens in the list of tokens sent
def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]

#??? TODO add comments
def remove_extras(tokens):
    return [token for token in tokens if token not in ['no_queri','no_narr']]

#preprocessing the text by turning it into "good" tokens
def preprocess_text(text):
    tokens = tokenize(text)
    tokens = stem_tokens(tokens)
    tokens = remove_extras(tokens)
    return tokens

#preprocessing all of the documents now
def preprocess_documents(documents):
    previous_id = 'x'
    count = 1

    #going through each document line by line and extracting information to tokenise it and put it back where it belongs.
    for doc in documents:
        file_id = str(doc['DOCNO'].split(" ")[0])
        if file_id != previous_id:
            previous_id = file_id
            count += 1
        doc['TEXT'] = preprocess_text(doc['TEXT'])
        doc['HEAD'] = preprocess_text(doc['HEAD'])

    return documents

#preprocessing queries
def preprocess_queries(queries):
    for query in queries:
        query['title'] = preprocess_text(query['title'])
        query['query'] = preprocess_text(query['query'])
        query['narrative'] = preprocess_text(query['narrative'])
    return queries

def save_preprocessed_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def load_preprocessed_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data