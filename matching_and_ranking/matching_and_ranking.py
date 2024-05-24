import math
from collections import defaultdict


class MatchingAndRanking:
    def __init__(self):
        None

    def match_and_rank_documents(self, query_terms, inverted_index, k=10):
        # Initialize document vectors and lengths
        document_vectors = defaultdict(lambda: defaultdict(int))
        document_lengths = {}

        # Populate document vectors and lengths from inverted index
        for term in inverted_index:
            for doc_id, weight in inverted_index[term]:
                document_vectors[doc_id][term] = weight
                document_lengths[doc_id] = document_lengths.get(doc_id, 0) + weight ** 2

        # Calculate document vector lengths
        for doc_id in document_lengths:
            document_lengths[doc_id] = math.sqrt(document_lengths[doc_id])

        # Create query vector
        query_vector = defaultdict(int)
        for term in query_terms:
            if term in inverted_index:
                query_vector[term] += 1  # Simple term frequency for query vector

        # Normalize query vector
        query_length = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))
        for term in query_vector:
            query_vector[term] /= query_length

        # Calculate cosine similarity between query and document vectors
        document_scores = {}
        for doc_id in document_vectors:
            dot_product = sum(query_vector[term] * document_vectors[doc_id][term] for term in query_vector)
            document_scores[doc_id] = dot_product / document_lengths[doc_id]

        # Sort documents by score in descending order
        ranked_documents = sorted(document_scores.items(), key=lambda item: item[1], reverse=True)

        # Return a list of document IDs with highest scores first
        return {doc_id: score for doc_id, score in ranked_documents[:k]}
