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

def games_to_play(request):
    return render(request, 'games-to-play.html')

def hamster_clicker(request):
    return render(request, 'clicker.html')

def art(request):
    return render(request, 'art.html')

def treasure(request):
    return render(request, 'treasure.html')

def error_page(request):
    return render(request, 'error-page.html')