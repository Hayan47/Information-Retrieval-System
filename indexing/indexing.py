from collections import defaultdict

class Indexing:
    def __init__(self):
        self.inverted_index = defaultdict(list)

    def build_inverted_index(self, documents, doc_ids):
        for doc_id, doc_vector in enumerate(documents):
            for term, weight in doc_vector.items():
                if weight > 0:
                    self.inverted_index[term].append((doc_ids[doc_id], weight))

        return self.inverted_index