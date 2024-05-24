from django.urls import path
from . import views  

urlpatterns = [
    path('process_data/', views.processDataset, name="process data"),
    path('evaluate_system/', views.evaluateSystem, name="evaluate system"),
]