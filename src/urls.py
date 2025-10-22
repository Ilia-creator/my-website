from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('football/', views.football, name='football'),
    path('swimming/', views.swimming, name='swimming'),
    path('programming/', views.programming, name='programming'),
    path('music/', views.music, name='music'),
    path('games/', views.games, name='games'),
]

