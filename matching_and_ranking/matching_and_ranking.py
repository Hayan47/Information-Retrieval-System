import math
from collections import defaultdict


class MatchingAndRanking:
    def __init__(self):
        None

    def match_and_rank_documents(self, query_terms, inverted_index, k=10):
        # Initialize document scores (default: 0)
        document_scores = {doc_id: 0 for doc_list in inverted_index.values() for doc_id, _ in doc_list}

        # Iterate through each query term
        for term in query_terms:
            # Check if the term exists in the inverted index
            if term in inverted_index:
                # Get the document postings for the term
                postings_list = inverted_index[term]
                # Update document scores based on TF-IDF weights
                for doc_id, weight in postings_list:
                    document_scores[doc_id] += weight

        # Sort documents by score in descending order
        ranked_documents = sorted(document_scores.items(), key=lambda item: item[1], reverse=True)

        # Return a list of document IDs with highest scores first
        return {doc_id: score for doc_id, score in ranked_documents[:k]}
