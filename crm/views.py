from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from .models import Order, StatusCrm
from .forms import OrderForm
from cms.models import CmsSlider
from price.models import PriceTable, PriceCard
from telebot.orders import notify_new_order

# Create your views here.
def first_page(request):
    slider_list = CmsSlider.objects.all()
    pc_1 = PriceCard.objects.get(pk=1)
    pc_2 = PriceCard.objects.get(pk=2)
    pc_3 = PriceCard.objects.get(pk=3)
    price_table = PriceTable.objects.all()
    form = OrderForm()
    dict_obj = { 'slider_list': slider_list,
                 'pc_1': pc_1,
                 'pc_2': pc_2,
                 'pc_3': pc_3,
                 'price_table': price_table,
                 'form': form,
                 }
    return render(request, 'shop.html', dict_obj)


def thanks_page(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.path, login_url='/login/')

        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            package_id = form.cleaned_data.get('package_id')
            contact_method = form.cleaned_data['contact_method']

            package = None
            if package_id:
                package = PriceCard.objects.filter(pk=package_id).first()

            new_status, _created = StatusCrm.objects.get_or_create(status_name='Новый')

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
                # Telegram не настроен или ошибка, но форма всё равно работает

            return render(request, 'thanks.html', {
                'name': name,
                'package': package,
                'contact_method': element.get_order_contact_method_display(),
            })
        else:
            # Form is invalid, return same page with errors
            return render(request, 'shop.html', {'form': form})
    else:
        return render(request, 'thanks.html')
