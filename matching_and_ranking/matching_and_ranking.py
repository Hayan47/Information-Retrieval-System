import math
from collections import defaultdict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from gensim.models import Word2Vec
from spellchecker import SpellChecker

class MatchingAndRanking:
    def __init__(self, dataset_name):
        self.model = Word2Vec.load(f"{dataset_name}_word2vec.model")
        self.doc_vectors = self.read_doc_vectors(f"{dataset_name}_doc_vectors")
        self.threshold = 1e-03
        self.similarity_threshold=0.0
        self.spell = SpellChecker()

    def get_query_vector(self, tokens):
        valid_tokens = [token for token in tokens if token in self.model.wv]
        if not valid_tokens:
            return None
        return np.mean([self.model.wv[token] for token in valid_tokens], axis=0)

    def match_and_rank_documents(self, query_terms, inverted_index, k=10):
        query_vector = self.get_query_vector(query_terms)
        
        #check if vector is non for out of vocabulary word:
        if query_vector is None or np.isnan(query_vector).any():
            print("Initial query vector is nan or empty, applying spell checking.")
            # Correct spelling and recompute query vector
            query_terms = self.correct_spelling(query_terms)
            print(query_terms)
            query_vector = self.get_query_vector(query_terms)
            print(query_vector)


        # If still nan or empty, use a default vector
        if query_vector is None or np.isnan(query_vector).any():
            print("Query vector is still nan or empty after spell checking, using default vector.")
            default_vector = np.zeros(self.model.vector_size)  # Adjust based on your model's vector size
            query_vector = default_vector




        
        # Step 1: Identify significant components in the query vector
        significant_components = [i for i, value in enumerate(query_vector) if abs(value) > self.threshold]
        # Step 2: Find relevant document IDs using the significant components from the query vector
        relevant_doc_ids = set()
        for component in significant_components:
            if str(component) in inverted_index:
                doc_ids = [doc_id for doc_id, _ in inverted_index[str(component)]]
                relevant_doc_ids.update(doc_ids)

        # Step 3: Filter doc_vectors to include only relevant documents
        filtered_doc_vectors = [(doc_id, vector) for doc_id, vector in self.doc_vectors if doc_id in relevant_doc_ids]
        if not filtered_doc_vectors:
            return []

        # Step 4: Prepare document IDs and vectors for cosine similarity calculation
        doc_ids, vectors = zip(*filtered_doc_vectors)
        
        # Step 5: Compute cosine similarities between the query vector and the document vectors
        similarities = cosine_similarity([query_vector], vectors)[0]
        
        # Step 6: Rank the document IDs based on the computed similarities
        ranked_indices = np.argsort(similarities)[::-1]
        
        # Step 7: Select the top-k documents based on the highest similarity scores
        ranked_doc_ids_scores = [(doc_ids[i], similarities[i]) for i in ranked_indices if similarities[i]>self.similarity_threshold]
        return ranked_doc_ids_scores

    def read_doc_vectors(self, filename):
        with open(filename, 'rb') as f:
            doc_vectors = pickle.load(f)
        return doc_vectors
    

    def correct_spelling(self, tokens):
        return [self.spell.correction(token) for token in tokens]