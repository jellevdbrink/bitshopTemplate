from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Categorie, Product, Klant, Bestelling, BestellingProduct


class ProductAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id', 'naam', 'categorie', 'zichtbaar', 'hoeveelheid', 'eenheid', 'state')


class BestellingAdmin(admin.ModelAdmin):
    list_display = ('id', 'klant', 'dag_ophalen', 'besteltijd')
    list_filter = ['dag_ophalen', 'besteltijd']


class KlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam', 'email', 'telnr')


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('naam', 'zichtbaar', 'icon')


class BestellingProductAdmin(admin.ModelAdmin):
    list_display = ('bestelling', 'product', 'extra_optie', 'aantal')


admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Klant, KlantAdmin)
admin.site.register(Bestelling, BestellingAdmin)
admin.site.register(BestellingProduct, BestellingProductAdmin)
