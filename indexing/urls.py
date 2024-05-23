from django.urls import path
from . import views

urlpatterns = [
    path('indexing/', views.indexing, name='indexing'),
]