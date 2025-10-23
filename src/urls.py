from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('football/', views.football, name='football'),
    path('swimming/', views.swimming, name='swimming'),
    path('programming/', views.programming, name='programming'),
    path('music/', views.music, name='music'),
    path('games/', views.games, name='games'),
    path('games_to_play/', views.games_to_play, name='games_to_play'),
    path('hamster_clicker/', views.hamster_clicker, name='hamster_clicker'),
    path('art/', views.art, name='art'),
    path('treasure/', views.treasure, name='treasure'),
    path('error/', views.error_page, name='error_page'),
]

