from django.shortcuts import render
from .models import Hamster

def game_view(request):
    hamsters = Hamster.objects.all()
    return render(request, 'clicker.html', {'hamsters': hamsters})
