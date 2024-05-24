
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('ir_admin/', admin.site.urls, name='dashboard'),
    path('api/v1/preprocessing/', include('preprocessing.urls')),
    path('api/v1/representation/', include('representation.urls')),
    path('api/v1/ir/', include('ir_controller.urls')),
    path('api/v1/indexing/', include('indexing.urls')),
    path('api/v1/queryprocessing/', include('queryprocessing.urls')),
    path('api/v1/matching_and_ranking/', include('matching_and_ranking.urls')),
    path('', include('ui.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/v1/admin_tools/', include('admin_tools.urls')),
    path('api/v1/evaluation/', include('evaluation.urls')),
]
