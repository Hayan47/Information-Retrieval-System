from django.http import JsonResponse
from .text_processing import TextProcessing
from preprocessing.data.dataset import load_dataset
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def preprocess_data(request):
    dataset_name = request.data.get('dataset_name')
    # Path to dataset
    dataset = load_dataset(dataset_name)
    # Instantiate TextProcessing class
    processor = TextProcessing()

    # Load and preprocess data
    dataset['text'] = dataset['text'].map(processor.preprocess_text)

    # Convert processed DataFrame to JSON response
    response_data = dataset.to_dict()

    return Response(response_data)
