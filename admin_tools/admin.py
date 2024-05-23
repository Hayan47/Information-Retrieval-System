from django.contrib import admin
from .views import processDataset
from django.urls import path, include
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Document
from django.contrib import messages
import requests
from django.shortcuts import render


@admin.action(description='Process Dataset And Store It')
def process_dataset(modeladmin, request, queryset):
    dataset_name = request.POST.get('dataset_name')
    if dataset_name:
        process_dataset_endpoint = 'http://localhost:8000/api/v1/ir/process/'
        process_dataset_response = requests.post(process_dataset_endpoint, {'dataset_name': dataset_name})
        if process_dataset_response.status_code == 200:
            modeladmin.message_user(request, 'Dataset processed and stored successfully!')
        else:
            error_message = process_dataset_response.json().get('error', 'Unknown error')
            modeladmin.message_user(request, f'Error occurred during processing: {error_message}', level=messages.ERROR)
    else:
        return render(request, 'process_dataset.html', {
                'title': 'Load Dataset',
                'app_label': modeladmin.model._meta.app_label,
                'opts': modeladmin.model._meta,
            })

process_dataset.short_description = "Process Dataset"


class DatasetAdmin(admin.ModelAdmin):
    actions = [process_dataset]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Document, DatasetAdmin)

