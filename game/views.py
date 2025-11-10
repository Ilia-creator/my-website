from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import PlayerProgress
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def hamster_clicker_user(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'clicker.html', {'username': username})

@login_required
@csrf_exempt
def save_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            progress, created = PlayerProgress.objects.get_or_create(user=request.user)

            progress.money = data.get('money', progress.money)
            progress.money_per_click = data.get('money_per_click', progress.money_per_click)
            progress.autoclicker_level = data.get('autoclicker_level', progress.autoclicker_level)

            progress.save()

            return JsonResponse({'status': 'success', 'message': 'Progress saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@login_required
def load_progress(request):
    progress, created = PlayerProgress.objects.get_or_create(user=request.user)
    return JsonResponse({
        'money': progress.money,
        'money_per_click': progress.money_per_click,
        'autoclicker_level': progress.autoclicker_level
    })


@login_required
def new_game(request):
    progress, created = PlayerProgress.objects.get_or_create(user=request.user)
    progress.money = 0
    progress.money_per_click = 1
    progress.autoclicker_level = 0
    progress.save()
    return JsonResponse({'status': 'reset'})


