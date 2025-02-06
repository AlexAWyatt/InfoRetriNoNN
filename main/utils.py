import math
import os

# Create dictionary keyed using document numbers where values are the 
# length of the given document in terms of tokens
def collect_doc_lengths(documents): 
    return {doc['DOCNO']:len(doc['TEXT']) for doc in documents}

