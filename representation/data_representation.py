from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class DataRepresentation:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def tfidf_representation(self, documents):
        return self.vectorizer.fit_transform(documents)
         

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()