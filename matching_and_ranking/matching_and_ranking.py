import math
from collections import defaultdict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from gensim.models import Word2Vec
from spellchecker import SpellChecker
from sklearn.preprocessing import MinMaxScaler

class MatchingAndRanking:
    def __init__(self, dataset_name):
        self.model = Word2Vec.load(f"{dataset_name}_word2vec.model")
        self.doc_vectors = self.read_doc_vectors(f"{dataset_name}_doc_vectors")
        self.bm25 = self.read_bm25(dataset_name)
        self.similarity_threshold=0.7
        self.spell = SpellChecker()
        self.bm25_weight=1
        self.word2vec_weight=1

    def get_query_vector(self, tokens):
        valid_tokens = [token for token in tokens if token in self.model.wv]
        if not valid_tokens:
            return None
        return np.mean([self.model.wv[token] for token in valid_tokens], axis=0)
    
    def get_bm25_scores(self, query_terms):
        return self.bm25.get_scores(query_terms)

    def match_and_rank_documents(self, query_terms, k=100):
        
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

        bm25_scores = self.get_bm25_scores(query_terms)
        # Normalize BM25 scores
        normalized_bm25_scores = self.normalize_scores(bm25_scores)

        # Get the top-k documents based on BM25 scores
        top_k_indices = np.argsort(normalized_bm25_scores)[::-1][:k]
        top_k_docs = [(self.doc_vectors[i][0], normalized_bm25_scores[i]) for i in top_k_indices]

        if not top_k_docs:
            return []

        # Get vectors of the top-k documents
        top_k_doc_ids = [doc_id for doc_id, _ in top_k_docs]
        top_k_vectors = [vector for doc_id, vector in self.doc_vectors if doc_id in top_k_doc_ids]

        # Compute cosine similarities between the query vector and the document vectors
        similarities = cosine_similarity([query_vector], top_k_vectors)[0]
        # Normalize Word2Vec similarities
        normalized_similarities = self.normalize_scores(similarities)   

        # Combine BM25 scores and Word2Vec similarities for final ranking
        combined_scores = {doc_id: (self.bm25_weight * bm25_score + self.word2vec_weight * normalized_similarities[i])/2
                        for i, (doc_id, bm25_score) in enumerate(top_k_docs)}

        # Sort documents by the combined score
        ranked_doc_ids_scores = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)
        
        # Apply similarity threshold and return top results
        final_ranked_docs = [(doc_id, score) for doc_id, score in ranked_doc_ids_scores if score > self.similarity_threshold]

        return final_ranked_docs



    def read_doc_vectors(self, filename):
        with open(filename, 'rb') as f:
            doc_vectors = pickle.load(f)
        return doc_vectors

    def read_bm25(self, dataset_name):
        with open(f'{dataset_name}_bm25_model.pkl', 'rb') as f:
            doc_vectors = pickle.load(f)
        return doc_vectors
    
    def correct_spelling(self, tokens):
        return [self.spell.correction(token) for token in tokens]
    
    # Define a function to normalize scores using MinMaxScaler
    def normalize_scores(self, scores):
        min_score = min(scores)
        max_score = max(scores)
        if max_score == min_score:
            # Avoid division by zero if all scores are the same
            return [0.5] * len(scores)
        return [(score - min_score) / (max_score - min_score) for score in scores]

    
