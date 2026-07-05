from django.contrib import admin
from django.utils.html import format_html
from .models import PriceCard, PriceTable, PriceCardImage


class PriceCardImageInline(admin.TabularInline):
    model = PriceCardImage
    extra = 1
    fields = ('image', 'order', 'get_image_preview')
    readonly_fields = ('get_image_preview',)

    def get_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 5px;" />',
                obj.image.url
            )
        return 'Нет изображения'
    get_image_preview.short_description = 'Превью'


class PriceCardAdmin(admin.ModelAdmin):
    inlines = [PriceCardImageInline]
    list_display = ('pc_title', 'pc_value', 'get_image_preview', 'image_count')
    list_filter = ('pc_title',)
    search_fields = ('pc_title', 'pc_description')
    fieldsets = (
        ('Основная информация', {
            'fields': ('pc_title', 'pc_description', 'pc_value')
        }),
        ('Основное изображение (для списка)', {
            'fields': ('pc_image', 'get_image_preview_large'),
            'description': 'Это изображение будет показано в списке карточек'
        }),
    )
    readonly_fields = ('get_image_preview_large',)

    def get_image_preview(self, obj):
        if obj.pc_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.pc_image.url
            )
        return 'Нет изображения'
    get_image_preview.short_description = 'Превью'

    def get_image_preview_large(self, obj):
        if obj.pc_image:
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 10px;" />',
                obj.pc_image.url
            )
        return 'Изображение не загружено'
    get_image_preview_large.short_description = 'Превью изображения'

    def image_count(self, obj):
        count = obj.images.count()
        return f"{count} изображение(й)"
    image_count.short_description = 'Дополнительные изображения'


class PriceTableAdmin(admin.ModelAdmin):
    list_display = ('pt_title', 'pt_old_price', 'pt_new_price')
    list_filter = ('pt_title',)
    search_fields = ('pt_title',)
    fieldsets = (
        ('Информация об услуге', {
            'fields': ('pt_title', 'pt_old_price', 'pt_new_price')
        }),
    )


admin.site.register(PriceCard, PriceCardAdmin)
admin.site.register(PriceTable, PriceTableAdmin)
admin.site.register(PriceCardImage)
