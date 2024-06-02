from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.models import LdaModel


class TopicModeling:
    def __init__(self, trigrams):
        self.corpus, self.dictionary = self.get_corpus(trigrams)
        self.lda_model = LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=5, passes=10, random_state=100,per_word_topics=True)

    
    def saveModel(self, dataset_name):
        self.lda_model.save(f"{dataset_name}_lda_model.gensim")
    
    
    def saveDictionary(self, dataset_name):
        self.dictionary.save(f"{dataset_name}_dictionary.dict")


    def get_corpus(self, trigrams):
        dictionary = Dictionary(trigrams)
        dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
        corpus = [dictionary.doc2bow(doc) for doc in trigrams]
        corpus = self.remove_low_vlaue_words(corpus, dictionary)
        return corpus, dictionary
    

    def remove_low_vlaue_words(self, corpus, dictionary):
        tfidf = TfidfModel(corpus, id2word=dictionary)
        low_value = 0.3
        low_value_words = []

        for i in range(0, len(corpus)):
            bow = corpus[i]
            tfidf_ids = [id for id, value in tfidf[bow]]
            bow_ids = [id for id, value in bow]
            low_value_words = [id for id, value in tfidf[bow] if value < low_value]
            words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids]

            new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]

            if new_bow:
                 corpus[i] = new_bow

        return corpus
