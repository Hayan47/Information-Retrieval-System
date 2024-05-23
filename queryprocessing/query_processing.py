from preprocessing.text_processing import TextProcessing


class QueryProcessing:

    def process_query(self, query):
        processor = TextProcessing()
        query_terms = processor.preprocess_text(query)
        return query_terms