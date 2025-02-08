import math
import os

# Create dictionary keyed using document numbers where values are the 
# length of the given document in terms of tokens
def collect_doc_lengths(documents): 
    return {doc['DOCNO']:len(doc['TEXT']) for doc in documents}

def get_token_counts(query_tokens):
    token_counts = {}
    for token in query_tokens:
        if token not in token_counts:
            token_counts[token] = 0
        token_counts[token] += 1
    
    return token_counts

# pair query numbers and query text into a dict for use in search function
def pair_usable_query(queries):

    usable_queries = {}

    for query in queries:
        usable_queries[query['num']] = query['query']
    
    return usable_queries