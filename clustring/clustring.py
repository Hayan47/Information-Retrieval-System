from gensim.models import LdaModel
import pickle

class Clustring:
    def __init__(self, dataset_name):
        self.lda_model = LdaModel.load(f"{dataset_name}_lda_model.gensim")
        

    def get_dominant_topic(self, corpus, n=5):
        dominant_topics = []
        for bow in corpus:
            topic_probs = self.lda_model.get_document_topics(bow)
            top_n = sorted(topic_probs, key=lambda x: x[1], reverse=True)[:n]
            topics = [t for t, score in top_n if score >= 0.3]
            dominant_topics.append(topics)
        return dominant_topics
    
    def saveTopicsList(self, dataset_name, topics_list):
        with open('topics_list.pkl', 'wb') as f:
            pickle.dump(topics_list, f)