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
            # Handle success case (e.g., show a success message)
            message = 'Dataset processing successful!'
        else:
            # Handle error case (e.g., display error message)
            message = 'Error occurred during processing: ' + process_dataset_response.json().get('error', 'Unknown error')
        return render(request, 'process_dataset.html', {'message': message})
    else:
        return render(request, 'process_dataset.html')


