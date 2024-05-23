from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import pickle
from django.contrib.admin.views.decorators import staff_member_required
import os
import pandas as pd
from django.conf import settings


@staff_member_required
@api_view(['POST'])
def process_data(request):
    dataset_name = request.data.get('dataset_name')
    if dataset_name:
        # Call the preprocessing service
        preprocess_endpoint = f'http://localhost:8000/api/v1/preprocessing/preprocess/'
        preprocess_response = requests.post(preprocess_endpoint, {'dataset_name': dataset_name})

        if preprocess_response.status_code == 200:
            preprocessed_data = preprocess_response.json()
            # print(preprocess_response.json())
            # Call the data representation service
            represent_endpoint = 'http://localhost:8000/api/v1/representation/represent/'
            represent_response = requests.post(represent_endpoint, json={'preprocessed_data': preprocessed_data})
            if represent_response.status_code == 200:
                vsm = represent_response.json()['vector_space_model']
                doc_ids = represent_response.json()['doc_ids']
                index_endpoint = 'http://localhost:8000/api/v1/indexing/indexing/'
                indexing_response = requests.post(index_endpoint, json={'vsm': vsm ,'doc_ids':doc_ids})
            
                if indexing_response.status_code == 200:
                    inverted_index = indexing_response.json()
                    write_inverted_index(inverted_index, 'inverted_index')
                    return Response({'success': True, 'index': indexing_response.json()})
                else:
                    return Response({'error': 'Error occurred indexing'}, status=represent_response.status_code)
            else:
                return Response({'error': 'Error occurred during data representation'}, status=represent_response.status_code)
        else:
            return Response({'error': 'Error occurred during preprocessing'}, status=preprocess_response.status_code)
    else:
        return Response({'error': 'Missing text data'}, status=400)
    

@api_view(['POST'])
def search(request):
    query = request.data.get('query')
    if query:
        # Retrieve the inverted index from storage
        try:
            inverted_index = read_inverted_index('inverted_index')
        except inverted_index.DoesNotExist:
            return Response({'error': 'Inverted index not found'}, status=404)
        
        query_processing_endpoint = f'http://localhost:8000/api/v1/queryprocessing/queryprocessing/'
        query_processing_response = requests.post(query_processing_endpoint, json={'query': query})
        if query_processing_response.status_code == 200:
            query_terms = query_processing_response.json()
            matching_and_ranking_endpoint = f'http://localhost:8000/api/v1/matching_and_ranking/matching_and_ranking/'
            matching_and_ranking_response = requests.post(matching_and_ranking_endpoint, json={'query_terms': query_terms,'inverted_index': inverted_index})

            if matching_and_ranking_response.status_code == 200:
                return Response(matching_and_ranking_response.json())
            else:
                return Response({'error': 'Missing query terms in request data'}, status=400)
        else:
            return Response({'error': 'Missing query in request data'}, status=400)

    return Response({'error': 'Invalid request method (use POST)'}, status=400)

def write_inverted_index(inverted_index, filename):
   with open(filename, 'wb') as file:
        pickle.dump(inverted_index, file)

def read_inverted_index(filename):
    with open(filename, 'rb') as file:
        inverted_index = pickle.load(file)
    return inverted_index


@api_view(['POST'])
def evaluate_system(request):
    dataset_name = request.data.get('dataset_name')
    if dataset_name:
        queries_path = os.path.join(settings.BASE_DIR, 'IR', 'static', 'datasets', f'{dataset_name}_queries.csv')
        # qrels_df = pd.read_csv(queries_path, names=['query_id', 'doc_id', 'relevance_score'])
        # qrels = qrels_df.set_index(['query_id', 'doc_id'])['relevance_score'].to_dict()
        # qrels = {k: dict(v) for k, v in qrels.groupby(level=0)}
        # print(qrels)
        queries_df = pd.read_csv(queries_path, names=['query_id', 'query_text'])
        queries = [tuple(x) for x in queries_df.values]
        # processed_queries = []
        matched_documents = []

        try:
            inverted_index = read_inverted_index('inverted_index')
        except inverted_index.DoesNotExist:
            return Response({'error': 'Inverted index not found'}, status=404)
        

        query_processing_endpoint = f'http://localhost:8000/api/v1/queryprocessing/queryprocessing/'
        for query_id, query_text in queries[:5]:
            query_processing_response = requests.post(query_processing_endpoint, json={'query': query_text})
            if query_processing_response.status_code == 200:
                print(f"Query '{query_text}' (ID: {query_id}) processed successfully.")
                # processed_queries.append(query_processing_response)

                query_terms = query_processing_response.json()
                matching_and_ranking_endpoint = f'http://localhost:8000/api/v1/matching_and_ranking/matching_and_ranking/'
                matching_and_ranking_response = requests.post(matching_and_ranking_endpoint, json={'query_terms': query_terms,'inverted_index': inverted_index})

                if matching_and_ranking_response.status_code == 200:
                    matched_documents.append(matching_and_ranking_response)
                else:
                    return Response({'error': 'Missing query terms in request data'}, status=400)

            else:
                return Response({'error': 'Missing query in request data'}, status=400)

        return Response(matching_and_ranking_response.json())

    
    return Response({'error': 'Invalid request method (use POST)'}, status=400)

    
    


