from django.db import models

# Create your models here.

class PriceCard(models.Model):
    pc_value = models.CharField(max_length=20, verbose_name='Цена')
    pc_title = models.CharField(max_length=200, verbose_name='Название', null=True)
    pc_description = models.CharField(max_length=200, verbose_name='Описание')
    # image for the price card; optional to avoid breaking existing data
    pc_image = models.ImageField(upload_to='pricecards/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.pc_title or f'Product #{self.pk}'

    def get_first_image(self):
        """Get the first image from the gallery or the main image"""
        gallery = self.images.all().first()
        if gallery:
            return gallery.image.url
        return self.pc_image.url if self.pc_image else None

    class Meta:
        verbose_name = 'Цены'
        verbose_name_plural = 'Цены'


class PriceCardImage(models.Model):
    card = models.ForeignKey(PriceCard, on_delete=models.CASCADE, verbose_name='Карточка', related_name='images')
    image = models.ImageField(upload_to='pricecards/', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return f"{self.card.pc_title} - изображение {self.order}"

    class Meta:
        verbose_name = 'Изображение карточки'
        verbose_name_plural = 'Изображения карточек'
        ordering = ['order']

class PriceTable(models.Model):
    pt_title = models.CharField(max_length=200, verbose_name='Услуга')
    pt_old_price = models.CharField(max_length=20, verbose_name='Старая цена')
    pt_new_price = models.CharField(max_length=20, verbose_name='Новая цена')

    def __str__(self):
        return self.pt_title

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'