from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .query_processing import QueryProcessing


@api_view(['POST'])
def queryProcessing(request):
    query = request.data.get('query')
    queryProcessing = QueryProcessing()
    query_terms = queryProcessing.process_query(query)
    return Response(query_terms)
 