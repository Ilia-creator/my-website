from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cms.models import CmsSlider
from price.models import PriceCard, PriceTable
from crm.forms import OrderForm

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

def play_learn(request):
    return render(request, 'playLearn.html')

def shop(request):
    slider_list = CmsSlider.objects.all()
    # Get all price cards and the price table; templates will iterate over them
    price_cards = PriceCard.objects.all()
    price_table = PriceTable.objects.all()

    initial = {}
    if request.user.is_authenticated:
        initial = {'name': request.user.username, 'phone': request.user.phone}
    form = OrderForm(initial=initial)

    context = {
        'slider_list': slider_list,
        'price_cards': price_cards,
        'price_table': price_table,
        'form': form,
    }
    return render(request, 'shop.html', context)


@login_required
def shop_profile(request):
    return render(request, 'shop_profile.html', {'user': request.user})


def shop_login(request):
    if request.user.is_authenticated:
        return redirect('shop')
    if request.method == 'POST':
        from users.forms import LoginForm
        form = LoginForm(data=request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())
            next_url = request.POST.get('next') or '/shop/'
            return redirect(next_url)
    else:
        from users.forms import LoginForm
        form = LoginForm()
    return render(request, 'shop_login.html', {'form': form})


def shop_register(request):
    if request.user.is_authenticated:
        return redirect('shop')
    if request.method == 'POST':
        from users.forms import RegisterForm
        form = RegisterForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            user = form.save()
            login(request, user)
            next_url = request.POST.get('next') or '/shop/'
            return redirect(next_url)
    else:
        from users.forms import RegisterForm
        form = RegisterForm()
    return render(request, 'shop_register.html', {'form': form})
