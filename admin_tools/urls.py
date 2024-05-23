from django.urls import path
from . import views  

urlpatterns = [
    path('process_data/', views.processDataset, name="process data"),
]