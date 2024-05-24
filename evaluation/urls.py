from django.urls import path
from . import views  

urlpatterns = [
    path('evaluating/', views.evaluate, name="evaluating"),
]