from django.urls import path
from . import views

urlpatterns = [
    path('matching_and_ranking/', views.matchingAndRanking, name='matching_and_ranking'),
    path('matching_and_ranking_for_evaluation/', views.matchingAndRankingForEvaluation, name='matching_and_ranking_for_evaluation'),
]