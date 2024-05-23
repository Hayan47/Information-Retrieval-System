from collections import defaultdict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .indexing import Indexing


@api_view(['POST'])
def indexing(request):
    if request.method == 'POST':
        vsm = request.data.get('vsm')
        doc_ids =request.data.get('doc_ids')
        indexing = Indexing()
        # Build inverted index from preprocessed documents
        inverted_index = indexing.build_inverted_index(vsm, doc_ids)

        return Response(inverted_index)
    else:
        return Response({'error': 'Missing vsm'}, status=400)