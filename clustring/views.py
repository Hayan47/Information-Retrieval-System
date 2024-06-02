from rest_framework.decorators import api_view
from rest_framework.response import Response
from .clustring import Clustring

@api_view(['POST'])
def clustring(request):
    corpus = request.data.get('corpus')
    dataset_name = request.data.get('dataset_name')
    if corpus:
        clustring = Clustring(dataset_name=dataset_name)
        document_topics = clustring.get_dominant_topic(corpus=corpus)
        clustring.saveTopicsList(dataset_name=dataset_name, topics_list=document_topics)
        return Response({'document_topics': document_topics})
    else:
        return Response({'error': 'Missing corpus'}, status=400)