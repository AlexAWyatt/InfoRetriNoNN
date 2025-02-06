import math
import os

class tf_idf:
    def __init__(self, inverted_index, doc_lengths):
        self.inverted_index = inverted_index
        self.doc_lengths = doc_lengths
        self.tot_docs = len(doc_lengths)
        
    # Normalized Term Frequency
    def norm_tf(self, term, doc_id):
        freq_doc = self.inverted_index[term][doc_id]
        return freq_doc/self.doc_lengths['doc_id']
    
    def idf(self, term):
        num_corp = self.tot_docs
        tot_contain = len(self.inverted_index[term])

        # Otherwise we would divide by zero - this is in lieue of using a corrections term
        # to prevent against dividing by 0 (only for safety)
        if tot_contain == 0:
            return 0

        # natural logarithn here - change if needed
        return math.log(num_corp/tot_contain)
    
    # calculate tf-idf got a given term in a given doc
    def score_term_doc(self, term, doc_id):
        return self.norm_tf(term, doc_id)*self.idf(term)
    
    # calculate tf-idf for given doc for all query terms
    def score_doc(self, doc_id, query):
        fin_score = 0

        for token in query:
            if token in self.inverted_index and doc_id in self.inverted_index[token]:
                fin_score += self.score_term_doc(token, doc_id)
        
        return fin_score


'''First version is going to be for a general application. Looking to improve to 
"zone specific" bm25F after - https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf'''
# inherit tf_idf as parent so we have idf method (ease of maintenance)
class BM25(tf_idf):
    def __init__(self, inverted_index, doc_lengths, k1, b):
        self.inverted_index = inverted_index
        self.doc_lengths = doc_lengths
        self.tot_docs = len(doc_lengths)
        self.k1 = k1
        self.b = b 
        self.dl = sum(doc_lengths.values())
        self.avdl = self.dl/self.tot_docs

    def __B(self):
        return (1-self.b)+(self.b*(self.dl/self.avdl))
    
    # calculate bm25 for a given term in a given doc
    def score_term_doc(self, term, doc_id):

        tf_prime = self.inverted_index[term][doc_id]/self.__B()
        idf = self.idf(term)
        return idf * (((self.k1 + 1)*tf_prime)/(self.k1 + tf_prime))
    
    # calculate bm25 for a given doc for all query terms
    def score_doc(self, doc_id, query):
        fin_score = 0

        for token in query:
            if token in self.inverted_index and doc_id in self.inverted_index[token]:
                fin_score += self.score_term_doc(token, doc_id)
        
        return fin_score







