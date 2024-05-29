from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import pickle
from django.contrib.admin.views.decorators import staff_member_required
import os
import pandas as pd
from django.conf import settings
from gensim.models import Word2Vec
import gzip


@staff_member_required
@api_view(['POST'])
def process_data(request):
    dataset_name = request.data.get('dataset_name')
    if dataset_name:
        print("Preprocessing")
        preprocess_endpoint = f'http://localhost:8000/api/v1/preprocessing/preprocess/'
        preprocess_response = requests.post(preprocess_endpoint, {'dataset_name': dataset_name})

        if preprocess_response.status_code == 200:
            preprocessed_data = preprocess_response.json()
            print("Representing")
            represent_endpoint = 'http://localhost:8000/api/v1/representation/represent/'
            represent_response = requests.post(represent_endpoint, json={'preprocessed_data': preprocessed_data, 'dataset_name': dataset_name})
            if represent_response.status_code == 200: 
                return Response({'success': True})  
                # print("Indexing")
                # index_endpoint = 'http://localhost:8000/api/v1/indexing/indexing/'
                # indexing_response = requests.post(index_endpoint, json={'dataset_name': dataset_name})
                # if indexing_response.status_code == 200:
                #     inverted_index = indexing_response.json()['inverted_index']
                #     save_inverted_index_chunked(inverted_index, 50,  f'{dataset_name}_inverted_index')
                #     return Response({'success': True, 'index': inverted_index})
                # else:
                #     return Response({'error': 'Error occurred indexing'}, status=represent_response.status_code)
            else:
                return Response({'error': 'Error occurred during data representation'}, status=represent_response.status_code)
        else:
            return Response({'error': 'Error occurred during preprocessing'}, status=preprocess_response.status_code)
    else:
        return Response({'error': 'Missing text data'}, status=400)
    

@api_view(['POST'])
def search(request):
    query = request.data.get('query')
    dataset_name = request.data.get('dataset_name')
    if query:
        # try:
        #     print("Reading Index")
        #     inverted_index = load_inverted_index_chunked(f'{dataset_name}_inverted_index')
        # except inverted_index.DoesNotExist:
        #     return Response({'error': 'Inverted index not found'}, status=404)
        print("Processing Query")
        query_processing_endpoint = f'http://localhost:8000/api/v1/queryprocessing/queryprocessing/'
        query_processing_response = requests.post(query_processing_endpoint, json={'query': query})
        if query_processing_response.status_code == 200:
            query_terms = query_processing_response.json()
            matching_and_ranking_endpoint = f'http://localhost:8000/api/v1/matching_and_ranking/matching_and_ranking/'
            matching_and_ranking_response = requests.post(matching_and_ranking_endpoint, json={'query_terms': query_terms,'dataset_name': dataset_name})
            print("Matching Query and Ranking Results")
            if matching_and_ranking_response.status_code == 200:
                return Response(matching_and_ranking_response.json())
            else:
                return Response({'error': 'Missing query terms in request data'}, status=400)
        else:
            return Response({'error': 'Missing query in request data'}, status=400)

    return Response({'error': 'Invalid request method (use POST)'}, status=400)


@api_view(['POST'])
def evaluate_system(request):
    dataset_name = request.data.get('dataset_name')
    if dataset_name:
        queries_path = os.path.join(settings.BASE_DIR, 'IR', 'static', 'datasets', f'{dataset_name}_queries.csv')
        queries_df = pd.read_csv(queries_path, names=['query_id', 'query_text'])
        queries = [tuple(x) for x in queries_df.values]
        matched_documents = {}
        # try:
        #     print("Reading Index")
        #     inverted_index = load_inverted_index_chunked(f'{dataset_name}_inverted_index')
        # except inverted_index.DoesNotExist:
        #     return Response({'error': 'Inverted index not found'}, status=404)
        query_processing_endpoint = f'http://localhost:8000/api/v1/queryprocessing/queryprocessing/'
        for query_id, query_text in queries[2:3]:
            query_processing_response = requests.post(query_processing_endpoint, json={'query': query_text})
            if query_processing_response.status_code == 200:
                print(f"Query '{query_text}' (ID: {query_id}) processed successfully.")
                query_terms = query_processing_response.json()
                matching_and_ranking_endpoint = f'http://localhost:8000/api/v1/matching_and_ranking/matching_and_ranking_for_evaluation/'
                matching_and_ranking_response = requests.post(matching_and_ranking_endpoint, json={'query_terms': query_terms, 'dataset_name': dataset_name})
                if matching_and_ranking_response.status_code == 200:
                    matched_documents[query_id] = matching_and_ranking_response.json()
                else:
                    return Response({'error': 'Missing query terms in request data'}, status=400)
            else:
                return Response({'error': 'Missing query in request data'}, status=400)
        
        print("Evaluating")
        evaluation_endpoint = f'http://localhost:8000/api/v1/evaluation/evaluating/'
        evaluation_response = requests.post(evaluation_endpoint, json={'system_results': matched_documents, 'dataset_name': dataset_name })
        if evaluation_response.status_code == 200:
            return Response(evaluation_response.json())
        else:
            return Response({'error': 'Missing system results in request data'}, status=400)
    
    return Response({'error': 'Invalid request method (use POST)'}, status=400)
    
    

def split_dict(dictionary, chunk_size):
    """Split a dictionary into chunks of specified size."""
    it = iter(dictionary.items())
    for i in range(0, len(dictionary), chunk_size):
        yield {k: v for k, v in zip(range(chunk_size), it)}

def save_inverted_index_chunked(inverted_index, chunk_size, file_prefix):
    chunks = split_dict(inverted_index, chunk_size)
    for i, chunk in enumerate(chunks):
        with gzip.open(f'{file_prefix}_{i}.pkl.gz', 'wb') as file:
            pickle.dump(chunk, file, protocol=pickle.HIGHEST_PROTOCOL)

def load_inverted_index_chunked(file_prefix):
    inverted_index = {}
    i = 0
    while os.path.exists(f'{file_prefix}_{i}.pkl.gz'):
        with gzip.open(f'{file_prefix}_{i}.pkl.gz', 'rb') as file:
            chunk = pickle.load(file)
            inverted_index.update(chunk)
        i += 1
    return inverted_index
