import pandas as pd
from gensim.models import Word2Vec
import numpy as np
import pickle
from rank_bm25 import BM25Okapi

class DataRepresentation:
    def __init__(self, documents):
        self.model = Word2Vec(sentences=documents, vector_size=100, window=5, min_count=1, workers=4)
        self.bm25 = BM25Okapi(documents)

    def compute_document_vector(self, doc):
        word_vectors = [self.model.wv[word] for word in doc if word in self.model.wv]
        if word_vectors:
            doc_vector = np.mean(word_vectors, axis=0)
        else:
            doc_vector = np.zeros(self.model.vector_size)
        return doc_vector
    

    def saveModel(self, dataset_name):
        self.model.save(f"{dataset_name}_word2vec.model")


    def write_doc_vectors(self, doc_vectors, filename):
        with open(filename, 'wb') as f:
            pickle.dump(doc_vectors, f)


    def saveBM25(self, dataset_name):
        with open(f'{dataset_name}_bm25_model.pkl', 'wb') as file:
            pickle.dump(self.bm25, file)
