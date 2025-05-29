from django.contrib import admin
from .models import Producto
from django.utils.html import format_html


admin.site.register(Producto)

# Register your models here.
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'imagen_tag')

    def imagen_tag(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.imagen.url)
        return "-"
    imagen_tag.short_description = 'Imagen'
