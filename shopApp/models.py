from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from image_cropping import ImageRatioField


class Categorie(models.Model):
    naam = models.CharField(verbose_name="Categorie naam", max_length=50)
    icon = models.CharField(verbose_name="Naam van het bijpassende icon (icons8.com -> iOS filled type)", max_length=50, default="question-mark")
    zichtbaar = models.BooleanField('Zichtbaar', default=True)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categorieën"

    def __str__(self):
        return self.naam


class Klant(models.Model):
    naam = models.CharField(max_length=100)
    email = models.EmailField()
    telnr = models.CharField('Telefoon nummer', max_length=12)

    class Meta:
        verbose_name = "Klant"
        verbose_name_plural = "Klanten"

    def __str__(self):
        return self.naam


class Product(models.Model):
    naam = models.CharField("Product naam", max_length=50)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name="Categorie", db_index=False)
    snijdbaar = models.BooleanField("Snijdbaar", default=False)
    hoeveelheid = models.PositiveIntegerField("Te bestellen per (bv. 1 st./50 gr.)", default=1, validators=[MinValueValidator(1)])
    zichtbaar = models.BooleanField('Zichtbaar', default=True)
    # min_value = models.PositiveIntegerField("Minimale waarde", default=1)

    EENHEID_CHOICES = [
        ('st.', 'st.'),
        ('gr.', 'gr.'),
    ]
    eenheid = models.CharField(
        verbose_name="Eenheid",
        max_length=3,
        choices=EENHEID_CHOICES,
        default='st.'
    )

    STATE_CHOICES = [
        ('niet_gestart', 'Niet Gestart'),
        ('bezig', 'Bezig'),
        ('probleem', 'Probleem'),
        ('voltooid', 'Voltooid'),
    ]
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default='niet_gestart'
    )

    foto = models.ImageField(verbose_name='Foto van product', upload_to='product_fotos', default='product_fotos/default_product.jpg')
    cropping = ImageRatioField('foto', '550x550')

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Producten"
        ordering = ['state']

    def __str__(self):
        return self.naam


class Bestelling(models.Model):
    besteltijd = models.DateTimeField(auto_now_add=True)
    producten = ArrayField(models.IntegerField())
    klant = models.ForeignKey(Klant, verbose_name="Geplaatst door", on_delete=models.CASCADE, db_index=False)
    dag_ophalen = models.DateField(verbose_name="Dag van ophalen", default=date(2022, 1, 1))
    # medewerker = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Bestelling"
        verbose_name_plural = "Bestellingen"
        ordering = ['-besteltijd']

    def __str__(self):
        return str(self.id) + " - " + self.klant.naam
