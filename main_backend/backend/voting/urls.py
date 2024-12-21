from django.urls import path
from .views import register, face_recognition_view

urlpatterns = [
    path('register/', register, name='register'),
    path('face_recognition/', face_recognition_view, name='face_recognition'),
]
