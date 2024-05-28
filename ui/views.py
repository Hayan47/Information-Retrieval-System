from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        dataset_name = request.POST.get('dataset_name')
        # Make a POST request to the search function in the ir_controller app
        url = f"http://127.0.0.1:8000/api/v1/ir/search/"
        data = {'query': query, 'dataset_name': dataset_name}
        response = requests.post(url, data=data)
        try:
            search_results = response.json()  # Parse JSON response
            context = {'search_results': search_results}  # Store results in context
        except:
            context = {'error': 'Error parsing search results'}  # Handle parsing error
    else:
        context = {}
        
    return render(request, 'search.html', context)