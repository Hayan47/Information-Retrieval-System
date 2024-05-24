from django.shortcuts import render
from django.contrib import admin
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
@api_view(['POST'])
def processDataset(request):
    if request.method == 'POST':
        dataset_name = request.POST.get('dataset_name')
        # Call the process_data function with the dataset name
        process_dataset_endpoint = f'http://localhost:8000/api/v1/ir/process/'
        process_dataset_response = requests.post(process_dataset_endpoint, {'dataset_name': dataset_name})
        if process_dataset_response.status_code == 200:
            return Response(process_dataset_response.json())
        else:
            return Response({'message': 'Error occurred during data processing'})
    else:
        return Response({'error': 'Invalid request method (use POST)'}, status=400)


@staff_member_required
@api_view(['POST'])
def evaluateSystem(request):
    if request.method == 'POST':
        dataset_name = request.POST.get('dataset_name')
        evaluateSystem_endpoint = f'http://localhost:8000/api/v1/ir/evaluate_system/'
        evaluateSystem_response = requests.post(evaluateSystem_endpoint, {'dataset_name': dataset_name})
        if evaluateSystem_response.status_code == 200:
            return Response(evaluateSystem_response.json())
        else:
            return Response({'message': 'Error occurred evaluate system'})
    else:
        return Response({'error': 'Invalid request method (use POST)'}, status=400)
