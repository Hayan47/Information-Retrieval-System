from collections import defaultdict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .indexing import Indexing


@api_view(['POST'])
def indexing(request):
    if request.method == 'POST':
        dataset_name = request.data.get('dataset_name')
        indexing = Indexing()
        doc_vectors = indexing.read_doc_vectors(f'{dataset_name}_doc_vectors')
        inverted_index = indexing.build_inverted_index(doc_vectors, dataset_name)
        return Response({'inverted_index': inverted_index})
    else:
        return Response({'error': 'Missing dataset_name'}, status=400)