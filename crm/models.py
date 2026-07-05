from django.db import models

# Create your models here.
class StatusCrm(models.Model):
    status_name = models.CharField(max_length=200, verbose_name='Название статуса', null=True)

    def __str__(self):
        return self.status_name or f'Status #{self.pk}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Order(models.Model):
    CONTACT_TELEGRAM = 'telegram'
    CONTACT_WHATSAPP = 'whatsapp'
    CONTACT_CHOICES = [
        (CONTACT_TELEGRAM, 'Telegram'),
        (CONTACT_WHATSAPP, 'WhatsApp'),
    ]

    order_dt = models.DateTimeField(auto_now=True)
    order_name = models.CharField(max_length=200, verbose_name= 'Имя')
    order_phone = models.CharField(max_length=200, verbose_name='Телефон')
    order_status = models.ForeignKey(StatusCrm, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Статус')
    order_package = models.ForeignKey('price.PriceCard', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга')
    order_contact_method = models.CharField(max_length=20, choices=CONTACT_CHOICES, default=CONTACT_TELEGRAM, verbose_name='Contact method')

    def __str__(self):
        return self.order_name or f'Order #{self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ComentCrm(models.Model):
    coment_binding = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заявка')
    coment_text = models.TextField(verbose_name='Текст комментария')
    coment_dt = models.DateTimeField(auto_now=True, verbose_name='Дата создания')

    def __str__(self):
        return self.coment_text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


