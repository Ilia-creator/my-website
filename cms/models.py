from django.db import models

class CmsSlider(models.Model):
    cms_img = models.ImageField(upload_to='sliderimg/', null=True, blank=True, verbose_name='Изображение')
    cms_title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Заголовок')
    cms_text = models.CharField(max_length=200, null=True, blank=True, verbose_name='Текст')
    cms_css = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name='CSS класс')

    def __str__(self):
        return self.cms_title or f'Slide #{self.pk}'

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
