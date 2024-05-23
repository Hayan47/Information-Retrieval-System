from django.urls import path
from . import views

urlpatterns = [
    path('represent/', views.represent_data, name='represent_data'),
]
