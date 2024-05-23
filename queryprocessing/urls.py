from django.urls import path
from . import views

urlpatterns = [
    path('queryprocessing/', views.queryProcessing, name='query_processing'),
]
