import pandas as pd
from gensim.models import Word2Vec
import numpy as np
import pickle

class DataRepresentation:
    def __init__(self, documents):
        self.model = Word2Vec(sentences=documents, vector_size=100, window=5, min_count=1, workers=4)

    def saveModel(self, dataset_name):
        self.model.save(f"{dataset_name}_word2vec.model")

    def compute_document_vector(self, doc):
        # Filter words in the document that are present in the model's vocabulary
        word_vectors = [self.model.wv[word] for word in doc if word in self.model.wv]
        if word_vectors:
            # Calculate the mean vector
            doc_vector = np.mean(word_vectors, axis=0)
        else:
            # Handle case where no words are in the vocabulary (e.g., return a zero vector or handle accordingly)
            doc_vector = np.zeros(self.model.vector_size)
        return doc_vector

    def write_doc_vectors(self, doc_vectors, filename):
        with open(filename, 'wb') as f:
            pickle.dump(doc_vectors, f)
