from django.urls import path
from .views import *

app_name = 'application'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('project-feature-add', project_feature_add_view, name='project-feature-add'),
    path('edit_view/<int:id>/', edit_view, name='edit_view'),
    path('delete_view/<int:id>/', delete_view, name='delete_view'),
    path('download_view/', download_view, name='download_view'),
    path('redesign-schema/', correctDB_view, name="correctDB_view"),
    path('save-response', save_response, name="save_response")
]