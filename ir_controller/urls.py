from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_data, name='process_data'),
    path('search/', views.search, name='search'),
    path('evaluate_system/', views.evaluate_system, name='evaluate_system'),
]