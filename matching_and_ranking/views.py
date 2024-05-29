from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .matching_and_ranking import MatchingAndRanking
from admin_tools.models import Document
from admin_tools.serializers import DocumentSerializer

@api_view(['POST'])
def matchingAndRanking(request):
    query_terms = request.data.get('query_terms')
    # inverted_index = request.data.get('inverted_index')
    dataset_name = request.data.get('dataset_name')
    matching_and_ranking = MatchingAndRanking(dataset_name=dataset_name)
    docs_list = matching_and_ranking.match_and_rank_documents(query_terms)
    print(docs_list)
    documents = []
    for doc_id, score in docs_list:
        try:
            document = Document.objects.get(doc_id=doc_id)
            documents.append(document)
        except Document.DoesNotExist:
            pass
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def matchingAndRankingForEvaluation(request):
    query_terms = request.data.get('query_terms')
    inverted_index = request.data.get('inverted_index')
    dataset_name = request.data.get('dataset_name')
    matching_and_ranking = MatchingAndRanking(dataset_name=dataset_name)
    docs_list = matching_and_ranking.match_and_rank_documents(query_terms)
   
    return Response(docs_list)
