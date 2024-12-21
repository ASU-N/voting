from django.urls import path
from .views import face_recognition_view

urlpatterns = [
    # other paths
    path('face_recognition/', face_recognition_view, name='face_recognition'),
]
