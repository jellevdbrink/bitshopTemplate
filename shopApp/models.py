from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models

from image_cropping import ImageRatioField


def get_empty_list_default():
    return []


class Klant(models.Model):
    naam = models.CharField('Naam', max_length=100)
    email = models.EmailField('E-mail', unique=True)
    telnr = models.CharField('Telefoon nummer', max_length=12)

    class Meta:
        verbose_name = "klant"
        verbose_name_plural = "klanten"

    def __str__(self):
        return self.naam


# ----- PRODUCTEN --------------------------------------------------------------

EENHEID_CHOICES = [
    ('st.', 'st.'),
    ('gr.', 'gr.'),
]

STATE_CHOICES = [
    ('niet_gestart', 'Niet Gestart'),
    ('bezig', 'Bezig'),
    ('probleem', 'Probleem'),
    ('voltooid', 'Voltooid'),
]


class Categorie(models.Model):
    naam = models.CharField(verbose_name="Categorie naam", max_length=50)
    icon = models.CharField(verbose_name="Icon", max_length=50, default="question-mark", help_text="icons8.com -> iOS filled type (bij geen foto: question-mark)")
    zichtbaar = models.BooleanField('Zichtbaar', default=True)

    class Meta:
        verbose_name = "categorie"
        verbose_name_plural = "categorieën"

    def __str__(self):
        return self.naam


class Product(models.Model):
    naam = models.CharField("Product naam", max_length=50)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name="Categorie", db_index=False)
    foto = models.ImageField(verbose_name='Foto van product', upload_to='product_fotos', default='product_fotos/default_product.jpg')
    beschrijving = models.TextField('Beschrijving product')
    extra_opties = ArrayField(models.CharField(max_length=50, default="", blank=True), default=get_empty_list_default)

    zichtbaar = models.BooleanField('Zichtbaar', default=True)
    # snijdbaar = models.BooleanField("Snijdbaar", default=False)

    hoeveelheid = models.PositiveIntegerField("Hoeveelheid", default=1, validators=[MinValueValidator(1)], help_text="bv. <1> st. / <100> gr.)")
    eenheid = models.CharField(verbose_name="Eenheid", max_length=3, choices=EENHEID_CHOICES, default='st.')
    min_aantal = models.PositiveIntegerField("Minimale aantal", default=1, help_text="Voor een product met een hoeveel van 50 gram en een min waarde van 100 gram, vul <2> in.")

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='niet_gestart')
    cropping = ImageRatioField('foto', '550x550')

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "producten"

    def __str__(self):
        return self.naam


#class MarineerProduct


# ----- BESTELLINGEN --------------------------------------------------------------

class Bestelling(models.Model):
    besteltijd = models.DateTimeField(auto_now_add=True)
    klant = models.ForeignKey(Klant, verbose_name="Geplaatst door", on_delete=models.CASCADE, db_index=False)
    dag_ophalen = models.DateField(verbose_name="Dag van ophalen", default=date(2022, 1, 1))
    # medewerker = models.CharField(max_length=50)

    class Meta:
        verbose_name = "bestelling"
        verbose_name_plural = "bestellingen"
        ordering = ['-besteltijd']

    def __str__(self):
        return str(self.id) + " - " + self.klant.naam


class BestellingProduct(models.Model):
    bestelling = models.ForeignKey(Bestelling, on_delete=models.CASCADE, verbose_name='Bestelling')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    aantal = models.PositiveIntegerField(verbose_name='Aantal')
    extra_optie = models.CharField(max_length=50, default="", blank=True)

    class Meta:
        verbose_name = "Bestelling product"
        verbose_name_plural = "Bestelling producten"

    def __str__(self):
        return f'Bestelling {self.bestelling.id} - Product {self.product.naam} {self.extra_optie} x{str(self.aantal)}'
