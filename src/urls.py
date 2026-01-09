from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from users import views_users
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
    path('register/', views_users.register_view, name='register'),
    path('login/', views_users.login_view, name='login'),
    path('logout/', views_users.logout_view, name='logout'),
    path('profile/', views_users.profile_view, name='profile'),
    path('hamster_clicker/', include('hamsters.urls')),
    path('game/', include('game.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

