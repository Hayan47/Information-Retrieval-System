from django.http import JsonResponse
from .data_representation import DataRepresentation
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def represent_data(request):
    preprocessed_data = request.data.get('preprocessed_data')
    if preprocessed_data:
        # Join tokens into documents
        documents = [' '.join(tokens) for tokens in preprocessed_data['text'].values()]

        data_representation = DataRepresentation()

        tfidf_matrix = data_representation.tfidf_representation(documents)
        feature_names = data_representation.get_feature_names()

        # Convert the TF-IDF matrix to a list of dictionaries (vector space model)
        vector_space_model = []

        for doc_idx in range(tfidf_matrix.shape[0]):
            doc_vector = tfidf_matrix[doc_idx]
            doc_dict = {feature_names[term_idx]: term_value for term_idx, term_value in zip(doc_vector.indices, doc_vector.data)}
            vector_space_model.append(doc_dict)
        return Response({
            'vector_space_model':vector_space_model,
            'doc_ids': preprocessed_data['doc_id'].values(),
        })
    else:
        return Response({'error': 'Missing preprocessed data'}, status=400)