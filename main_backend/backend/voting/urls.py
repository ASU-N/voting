from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/elections/', views.home, name='home'),
    path('api/elections/<int:election_id>/', views.election_detail, name='election_detail'),
    path('api/elections/<int:election_id>/vote/', views.vote, name='vote'),
    path('api/elections/<int:election_id>/results/', views.election_results, name='election_results'),
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.user_login, name='login'),
    path('api/logout/', views.user_logout, name='logout'),
]
