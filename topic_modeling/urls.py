from django.urls import path
from . import views

urlpatterns = [
    path('topic_modeling/', views.topic_modeling, name='topic_modeling'),
]
