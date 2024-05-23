from django.urls import path
from . import views

urlpatterns = [
    path('preprocess/', views.preprocess_data, name='preprocess_text'),
]