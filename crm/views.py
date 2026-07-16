from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from .models import Order, StatusCrm
from .forms import OrderForm
from price.models import PriceCard
from telebot.orders import notify_new_order


def thanks_page(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.path, login_url='/shop/login/')

        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            package_id = form.cleaned_data.get('package_id')
            contact_method = form.cleaned_data['contact_method']

            package = None
            if package_id:
                package = PriceCard.objects.filter(pk=package_id).first()

            new_status, _ = StatusCrm.objects.get_or_create(status_name='Новый')

            element = Order(
                order_name=name,
                order_phone=phone,
                order_package=package,
                order_status=new_status,
                order_contact_method=contact_method,
            )
            element.save()

            try:
                notify_new_order(element)
            except Exception as e:
                print(f"Telegram send error: {e}")

            return render(request, 'thanks.html', {
                'name': name,
                'package': package,
                'contact_method': element.get_order_contact_method_display(),
            })
        else:
            return render(request, 'shop.html', {'form': form})
    else:
        return render(request, 'thanks.html')
