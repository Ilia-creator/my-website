from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save_progress, name='save_progress'),
    path('load/', views.load_progress, name='load_progress'),
    path('new/', views.new_game, name='new_game'),
]
