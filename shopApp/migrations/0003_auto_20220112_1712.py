# Generated by Django 3.2.9 on 2022-01-12 16:12

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0002_auto_20220112_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '550x550', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='product',
            name='hoeveelheid',
            field=models.IntegerField(default=1, verbose_name='Te bestellen per (bv. 1 st./50 gr.)'),
        ),
    ]