from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .evaluation import Evaluation

@api_view(['POST'])
def evaluate(request):
    dataset_name = request.data.get('dataset_name')
    system_results = request.data.get('system_results')

    evaluation = Evaluation()
    overall_metrics = evaluation.evaluate(system_results=system_results, dataset_name=dataset_name)
   
    return Response(overall_metrics)
