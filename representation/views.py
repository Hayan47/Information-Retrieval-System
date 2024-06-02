from django.http import JsonResponse
from .data_representation import DataRepresentation
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

@api_view(['POST'])
def represent_data(request):
    preprocessed_data = request.data.get('preprocessed_data')
    dataset_name = request.data.get('dataset_name')
    if preprocessed_data:
        documents = preprocessed_data['text'].values()
        dataRepresentation = DataRepresentation(documents=documents)
        dataRepresentation.saveModel(dataset_name)
        dataRepresentation.saveBM25(dataset_name)
        df = pd.DataFrame.from_dict(preprocessed_data)
        doc_vectors = [(row['doc_id'], dataRepresentation.compute_document_vector(row['text'])) for _, row in df.iterrows()]
        dataRepresentation.write_doc_vectors(filename = f'{dataset_name}_doc_vectors', doc_vectors = doc_vectors)
        trigrams = dataRepresentation.trigrams
        return Response({'trigrams':trigrams})
    else:
        return Response({'error': 'Missing preprocessed data'}, status=400)