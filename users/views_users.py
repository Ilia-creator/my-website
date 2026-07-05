from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def _safe_next(request, default='profile'):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and next_url.startswith('/'):
        return next_url
    return default


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(_safe_next(request))
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(_safe_next(request))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('home')

# Create your views here.
