from django.db import models

class PriceCard(models.Model):
    pc_value = models.CharField(max_length=20, null=True, blank=True, verbose_name='Цена')
    pc_title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название')
    pc_description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Описание')
    pc_image = models.ImageField(upload_to='pricecards/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.pc_title or f'Product #{self.pk}'

    def get_first_image(self):
        gallery = self.images.all().first()
        if gallery:
            return gallery.image.url
        return self.pc_image.url if self.pc_image else None

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class PriceCardImage(models.Model):
    card = models.ForeignKey(PriceCard, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='pricecards/', null=True, blank=True, verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return f'{self.card} — image {self.order}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order']


class PriceTable(models.Model):
    pt_title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название')
    pt_old_price = models.CharField(max_length=20, null=True, blank=True, verbose_name='Старая цена')
    pt_new_price = models.CharField(max_length=20, null=True, blank=True, verbose_name='Новая цена')

    def __str__(self):
        return self.pt_title or f'Price #{self.pk}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
