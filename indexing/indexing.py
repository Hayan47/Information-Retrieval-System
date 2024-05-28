from collections import defaultdict
from gensim.models import Word2Vec
import pickle
import numpy as np

class Indexing:
    def __init__(self):
        self.inverted_index = defaultdict(list)
        self.threshold = 1e-03


    def build_inverted_index(self, doc_vectors, dataset_name):
        for doc_id, vector in doc_vectors:
            for i, value in enumerate(vector):
                if abs(value) > self.threshold:
                    self.inverted_index[i].append((doc_id, np.float16(value)))
        return self.inverted_index
    
    def read_doc_vectors(self, filename):
        with open(filename, 'rb') as f:
            doc_vectors = pickle.load(f)
        return doc_vectors