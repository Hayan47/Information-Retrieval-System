from rest_framework.decorators import api_view
from rest_framework.response import Response
from .modeling import TopicModeling

@api_view(['POST'])
def topic_modeling(request):
    trigrams = request.data.get('trigrams')
    dataset_name = request.data.get('dataset_name')
    if trigrams:
        topicModeling = TopicModeling(trigrams=trigrams)
        topicModeling.saveModel(dataset_name=dataset_name)
        topicModeling.saveDictionary(dataset_name=dataset_name)
        corpus = topicModeling.corpus
        return Response({'corpus':corpus})
    else:
        return Response({'error': 'Missing trigrams'}, status=400)