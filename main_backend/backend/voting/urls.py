from django.urls import path, include
from .views import register, face_recognition_view, get_candidates, cast_vote, get_results, CustomTokenView  # Ensure CustomTokenView is imported
from Aju.ovs.views import register_voter_view, login_view # Use the absolute import path

urlpatterns = [
    path('register/', register_voter_view, name='register_voter'), 
    path('login/', login_view, name='login'),
    path('face_recognition/', face_recognition_view, name='face_recognition'),
    path('get_candidates/', get_candidates, name='get_candidates'),
    path('cast_vote/', cast_vote, name='cast_vote'),
    path('get_results/', get_results, name='get_results'),
    path('o/token/', CustomTokenView.as_view(), name='custom_token'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
