from django.urls import path
from .views import register, face_recognition_view, get_candidates, cast_vote, get_results
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', register, name='register'),
    path('face_recognition/', face_recognition_view, name='face_recognition'),
    path('get_candidates/', get_candidates, name='get_candidates'),  # URL for fetching candidates
    path('cast_vote/', cast_vote, name='cast_vote'),
    path('get_results/', get_results, name='get_results'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh' ),
]
