from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def football(request):
    return render(request, 'football.html')

def swimming(request):
    return render(request, 'swimming.html')

def programming(request):
    return render(request, 'programming.html')

def music(request):
    return render(request, 'music.html')

def games(request):
    return render(request, 'games.html')